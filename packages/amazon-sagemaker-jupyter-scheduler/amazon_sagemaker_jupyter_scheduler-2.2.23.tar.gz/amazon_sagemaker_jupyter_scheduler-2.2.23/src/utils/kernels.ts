import isString from 'lodash/isString';
import { KERNELSPEC_NAME_SEPARATOR } from '../constants';
import { ParsedSpecName } from '../types';

export function parseSpecName(name: string | undefined): ParsedSpecName {
  // Parse a kernelspec into different parts
  // 1P Image kernelspec: {kernelname}__SAGEMAKER_INTERNAL__arn:aws:sagemaker:region:account:image/{imagename}
  // Custom Image kernelspec: {kernelname}__SAGEMAKER_INTERNAL__arn:aws:sagemaker:region:account:image-version/{imagename}/{version}
  // SMD kernelspec: {kernelname}__SAGEMAKER_INTERNAL__arn:aws:sagemaker:region:account:image/{imagename}__SAGEMAKER_INTERNAL__{imageversionalias}
  // Parsed result: { kernel: kernelname, arnEnvironment: arn:aws:sagemaker:region:account:image/imagename/version, version: version }
  try {
    if (!isString(name) || name.length === 0) {
      return { kernel: null, arnEnvironment: null, version: null, imageVersionAlias: null };
    }

    const splitName = name.split(KERNELSPEC_NAME_SEPARATOR);
    const [kernel, environment, imageVersionAlias] = splitName;
    const splitEnv = environment && environment.split('/');

    const arnEnvironment = splitEnv && splitEnv[0] + '/' + splitEnv[1];
    const version = splitEnv.length === 3 ? splitEnv[2] : null;
    const arnEnvironmentWithVersion = version
      ? `${arnEnvironment}/${version}`
      : imageVersionAlias
      ? `${arnEnvironment}${KERNELSPEC_NAME_SEPARATOR}${imageVersionAlias}`
      : arnEnvironment;

    return { kernel, arnEnvironment: arnEnvironmentWithVersion, version, imageVersionAlias: imageVersionAlias ?? null };
  } catch (e) {
    return { kernel: null, arnEnvironment: null, version: null, imageVersionAlias: null };
  }
}
