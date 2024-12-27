interface ParsedSpecName {
  kernel: string | null;
  arnEnvironment: string | null;
  /** version for custom images */
  version: string | null;
  /** image version alias for SMD images */
  imageVersionAlias: string | null;
}

export { ParsedSpecName };
