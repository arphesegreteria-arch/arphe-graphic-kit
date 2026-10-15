import { access, readFile } from 'node:fs/promises';
import path from 'node:path';

import { BrandValidationError } from './brand-loader.js';

export class SpecificationValidationError extends Error {
  constructor(message) {
    super(message);
    this.name = 'SpecificationValidationError';
  }
}

function isInside(root, target) {
  const relative = path.relative(root, target);
  return relative === '' || (!relative.startsWith(`..${path.sep}`) && relative !== '..' && !path.isAbsolute(relative));
}

export function resolveSafePath({ rendererRoot, baseDirectory = rendererRoot, requestedPath, label }) {
  if (typeof requestedPath !== 'string' || requestedPath.trim() === '') {
    throw new SpecificationValidationError(`${label} deve essere un percorso non vuoto`);
  }
  const resolved = path.resolve(baseDirectory, requestedPath);
  if (!isInside(path.resolve(rendererRoot, '..'), resolved)) {
    throw new SpecificationValidationError(`${label} esce dal repository: ${requestedPath}`);
  }
  return resolved;
}

export async function readOptionalAsset(options) {
  if (options.requestedPath == null) return null;
  const file = resolveSafePath(options);
  const extension = path.extname(file).toLowerCase();
  if (!['.png', '.jpg', '.jpeg', '.webp', '.svg'].includes(extension)) {
    throw new SpecificationValidationError(`${options.label} ha estensione non supportata: ${extension || '(nessuna)'}`);
  }
  try {
    await access(file);
    return { file, contents: await readFile(file) };
  } catch {
    throw new SpecificationValidationError(`${options.label} mancante o non leggibile: ${file}`);
  }
}

export function validateSpecification(specification) {
  if (!specification || typeof specification !== 'object' || Array.isArray(specification)) {
    throw new SpecificationValidationError('la specifica deve essere un oggetto JSON');
  }
  const unknownKeys = Object.keys(specification).filter((key) => !['brand', 'template', 'width', 'height', 'title', 'subtitle', 'background', 'output'].includes(key));
  if (unknownKeys.length) throw new SpecificationValidationError(`chiavi non supportate: ${unknownKeys.join(', ')}`);
  if (specification.brand !== 'arphe') throw new SpecificationValidationError('brand supportato richiesto: arphe');
  if (!['youtube-thumbnail', 'instagram-post'].includes(specification.template)) {
    throw new SpecificationValidationError('template non supportato');
  }
  if (typeof specification.title !== 'string' || specification.title.trim() === '') {
    throw new SpecificationValidationError('title è obbligatorio e non può essere vuoto');
  }
  if (specification.subtitle != null && typeof specification.subtitle !== 'string') {
    throw new SpecificationValidationError('subtitle deve essere una stringa');
  }
  if (typeof specification.output !== 'string' || !specification.output.toLowerCase().endsWith('.png')) {
    throw new SpecificationValidationError('output è obbligatorio e deve terminare in .png');
  }
  if (specification.width != null && (!Number.isInteger(specification.width) || specification.width <= 0)) {
    throw new SpecificationValidationError('width deve essere un intero positivo');
  }
  if (specification.height != null && (!Number.isInteger(specification.height) || specification.height <= 0)) {
    throw new SpecificationValidationError('height deve essere un intero positivo');
  }
  return specification;
}

export function asBrandError(error) {
  if (error instanceof SpecificationValidationError || error instanceof BrandValidationError) return error;
  return new SpecificationValidationError(error.message);
}
