import { JobsView } from '@jupyterlab/scheduler';
import { ContentsManager, KernelSpec } from '@jupyterlab/services';
import { JSONObject } from '@lumino/coreutils';
import isString from 'lodash/isString';
import { DropdownItem } from '../../../components/selectinput';
import { KERNELSPEC_NAME_SEPARATOR } from '../../../constants';
import { parseSpecName } from '../../../utils';
import { RuntimeEnvParams } from '../initialValueHelpers';

const constructArnName = (env: string, kernel: string, version: string | null) => {
  const scrubbedVersion = version ? `/${version}` : '';

  return `${kernel}${KERNELSPEC_NAME_SEPARATOR}${env}${scrubbedVersion}`;
};

const AXIS_IMAGE_NAME = 'Geospatial';

const EMR_COMPATIBLE_IMAGES_LIST = [
  'datascience-1.0',
  'sagemaker-data-science-38',
  '1.8.1-cpu-py36',
  'pytorch-1.8-gpu-py36',
  'sagemaker-sparkmagic',
  'tensorflow-2.6-cpu-py38-ubuntu20.04-v1',
  'tensorflow-2.6-gpu-py38-cu112-ubuntu20.04-v1',
  'sagemaker-sparkanalytics-v1',
];

enum ImageGroup {
  Custom = 'customImage',
  Sagemaker = 'smeImage',
  Session = 'session',
}

interface ImageMapValue {
  kernelOptions: DropdownItem[];
  versionOptions: DropdownItem[];
  arnEnvironment: string;
  label: string;
  group: ImageGroup;
  description?: string;
  imageVersionAlias: string | null;
}

export async function getPreSelectedNotebookKernelSpec(filePath: string,
  contentsManager: ContentsManager): Promise<string> {
  if (filePath.endsWith('.ipynb')) {
    try {
      const notebookContent = await contentsManager.get(filePath);
      return notebookContent.content.metadata.kernelspec.name;
    } catch (e) {
      return '';
    }
  }
  return '';
};

interface ParsedSpecDisplayName {
  imageName: string | null;
  kernelName: string | null;
}

function parseSpecDisplayName(displayName: string | undefined): ParsedSpecDisplayName {
  try {
    if (!isString(displayName) || displayName.length === 0) {
      return { imageName: null, kernelName: null };
    }

    const [kernelPart, imagePart] = displayName.split('(');
    const imageName = imagePart && imagePart.slice(0, -1).split('/')[0];
    const kernelName = kernelPart && kernelPart.slice(0, -1);

    return { imageName, kernelName };
  } catch (e) {
    // TODO @mgoguen add logging here if / when possible
    return { imageName: null, kernelName: null };
  }
}

const OPTION_GROUP_LABELS: { [key: string]: string } = {
  smeImage: 'Sagemaker Image',
  customImage: 'Custom Image',
  prefered: 'Use image from preferred session',
  session: 'Use image from other session',
};

function getImageOptionsFromMap(
  imageMap: { [key: string]: ImageMapValue },
  group: ImageGroup,
  isFromCluster?: boolean,
): DropdownItem {
  const filteredImages = Object.values(imageMap).filter((img) => {
    const env = img.arnEnvironment.split('/')[1];
    // If notebook is open from a cluster, only show EMR compatible images
    if (isFromCluster) {
      return img?.group === group && EMR_COMPATIBLE_IMAGES_LIST.includes(env);
    }

    // filter out axis image
    if (img?.group === ImageGroup.Sagemaker && img.label.includes(AXIS_IMAGE_NAME)) {
      return false;
    }

    // Show the image if the group matches
    return img?.group === group;
  });

  return {
    label: OPTION_GROUP_LABELS[group],
    value: '',
    options: filteredImages.map((img) => ({
      label: img.label,
      value: group === ImageGroup.Session ? img.label : img.arnEnvironment,
      group: OPTION_GROUP_LABELS[group],
      optionMetadata: img,
      options: img.versionOptions,
    })),
  };
}

export const getInitialImageValueForStudio = (
  runtimeEnvironmentParameters: RuntimeEnvParams,
  preSelectedKernelFromNotebook: string | undefined,
  view: JobsView
) => {
  if (view === JobsView.JobDetail || view === JobsView.JobDefinitionDetail) {
    if (runtimeEnvironmentParameters) {
      const { sm_kernel, sm_image } = runtimeEnvironmentParameters;
      const KERNEL_IMAGE_KEY = `${sm_kernel}__SAGEMAKER_INTERNAL__${sm_image}`;

      return parseSpecName(KERNEL_IMAGE_KEY);
    }

    return {
      kernel: null,
      arnEnvironment: null,
      version: null,
      imageVersionAlias: null
    };
  } else if (view === JobsView.CreateForm) {
    if (
      runtimeEnvironmentParameters &&
      'sm_image' in runtimeEnvironmentParameters
    ) {
      const { sm_kernel, sm_image } = runtimeEnvironmentParameters;
      const KERNEL_IMAGE_KEY = `${sm_kernel}__SAGEMAKER_INTERNAL__${sm_image}`;
      return parseSpecName(KERNEL_IMAGE_KEY);
    }

    return (
      parseSpecName(preSelectedKernelFromNotebook) || {
        kernel: null,
        arnEnvironment: null,
        version: null,
        imageVersionAlias: null
      }
    );
  }

  return (
    parseSpecName(preSelectedKernelFromNotebook) || {
      kernel: null,
      arnEnvironment: null,
      version: null,
      imageVersionAlias: null
    }
  );
};


export function getImagesFromMap(options: KernelSpec.ISpecModels): Record<string, ImageMapValue> {
  const imageMap: { [key: string]: ImageMapValue } = {};
  const specs = options.kernelspecs;

  Object.values(specs).forEach((spec: any) => {
    if (!spec) {
      return;
    }

    const smeMetadata = spec.spec?.metadata
      ? (spec.spec.metadata.sme_metadata as JSONObject)
      : null;

    const { imageName, kernelName } = parseSpecDisplayName(
      spec.spec.display_name
    );
    const { kernel, arnEnvironment, version, imageVersionAlias } = parseSpecName(spec.name);

    const versionOrImageVersionAlias = version ?? imageVersionAlias;

    // If parsing failed, something is wrong, so skip. Only version can be null after parsing.
    if (!kernel || !arnEnvironment || !imageName || !kernelName) {
      return;
    }

    const imageLabel = versionOrImageVersionAlias ? `${imageName} v${versionOrImageVersionAlias}` : imageName;

    const specMetaData: ImageMapValue = {
      arnEnvironment,
      kernelOptions: [{ label: kernelName, value: kernel }],
      imageVersionAlias,
      versionOptions: versionOrImageVersionAlias
        ? [{ label: `v${versionOrImageVersionAlias}`, value: versionOrImageVersionAlias }]
        : [],
      label: imageLabel,
      description: smeMetadata?.description
        ? (smeMetadata.description as string)
        : undefined,
      group: smeMetadata && smeMetadata.is_template ? ImageGroup.Sagemaker : ImageGroup.Custom,
    };

    if (!imageMap[arnEnvironment]) {
      imageMap[arnEnvironment] = specMetaData;
    } else {
      const { kernelOptions } = imageMap[arnEnvironment];
      if (!kernelOptions.some(opt => opt.value === kernel)) {
        const newKernelOptions = [
          ...kernelOptions,
          { label: kernelName, value: kernel } as DropdownItem
        ];
        imageMap[arnEnvironment].kernelOptions = newKernelOptions;
      }

      if (versionOrImageVersionAlias) {
        const { versionOptions } = imageMap[arnEnvironment];
        if (!versionOptions?.some(opt => opt.value === versionOrImageVersionAlias)) {
          const optionToAdd = {
            label: `v${versionOrImageVersionAlias}`,
            value: versionOrImageVersionAlias.toString()
          };

          const newVersionOptions = Array.isArray(versionOptions)
            ? [...versionOptions, optionToAdd]
            : [optionToAdd];

          imageMap[arnEnvironment].versionOptions = newVersionOptions;
        }
      }
    }
  });

  return imageMap;
}

export {
  constructArnName,
  parseSpecName,
  parseSpecDisplayName,
  getImageOptionsFromMap,
  ImageGroup,
  ImageMapValue,
};
