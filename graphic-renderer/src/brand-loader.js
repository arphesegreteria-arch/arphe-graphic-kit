import { access, readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export class BrandValidationError extends Error {
  constructor(message) {
    super(message);
    this.name = 'BrandValidationError';
  }
}

const moduleRoot = path.dirname(fileURLToPath(import.meta.url));
const defaultRendererRoot = path.resolve(moduleRoot, '..');

function mergeBrand(base, overrides = {}) {
  return {
    ...base,
    ...overrides,
    colors: { ...base.colors, ...overrides.colors },
    fonts: {
      ...base.fonts,
      ...overrides.fonts,
      title: { ...base.fonts.title, ...overrides.fonts?.title, source: { ...base.fonts.title.source, ...overrides.fonts?.title?.source } },
      body: { ...base.fonts.body, ...overrides.fonts?.body, source: { ...base.fonts.body.source, ...overrides.fonts?.body?.source } },
    },
    logos: {
      ...base.logos,
      ...overrides.logos,
      ink: { ...base.logos.ink, ...overrides.logos?.ink },
      cream: { ...base.logos.cream, ...overrides.logos?.cream },
    },
  };
}

async function requireFile(file, label) {
  try {
    await access(file);
  } catch {
    throw new BrandValidationError(`${label} mancante o non leggibile: ${file}`);
  }
}

function resolveBrandFile(rendererRoot, relativePath) {
  if (typeof relativePath !== 'string' || path.isAbsolute(relativePath)) {
    throw new BrandValidationError(`percorso brand non relativo: ${String(relativePath)}`);
  }
  const resolved = path.resolve(rendererRoot, relativePath);
  const repositoryRoot = path.resolve(rendererRoot, '..');
  const relative = path.relative(repositoryRoot, resolved);
  if (relative === '..' || relative.startsWith(`..${path.sep}`) || path.isAbsolute(relative)) {
    throw new BrandValidationError(`percorso brand esce dal repository: ${relativePath}`);
  }
  return resolved;
}

export async function loadBrand({ rendererRoot = defaultRendererRoot, overrides } = {}) {
  const configPath = path.join(rendererRoot, 'brand.json');
  let config;
  try {
    config = JSON.parse(await readFile(configPath, 'utf8'));
  } catch (error) {
    throw new BrandValidationError(`brand.json non leggibile: ${error.message}`);
  }

  const brand = mergeBrand(config, overrides);
  const colorsPath = resolveBrandFile(rendererRoot, brand.colors.file);
  await requireFile(colorsPath, 'token colori');
  try {
    brand.colors = JSON.parse(await readFile(colorsPath, 'utf8'));
  } catch (error) {
    throw new BrandValidationError(`token colori non validi: ${error.message}`);
  }
  const canonicalColorNames = ['cream', 'brown', 'burgundy', 'red', 'ink'];
  if (Object.keys(brand.colors).sort().join(',') !== canonicalColorNames.sort().join(',') || Object.values(brand.colors).some((value) => typeof value !== 'string' || !/^#[0-9A-F]{6}$/i.test(value))) {
    throw new BrandValidationError('token colori non conformi alla palette ARPHÈ');
  }

  brand.rendererRoot = rendererRoot;
  brand.fonts.title.source.file = resolveBrandFile(rendererRoot, brand.fonts.title.source.file);
  await requireFile(brand.fonts.title.source.file, 'font titolo originale');

  for (const [name, logo] of Object.entries(brand.logos)) {
    logo.file = resolveBrandFile(rendererRoot, logo.file);
    if (logo.required) await requireFile(logo.file, `logo obbligatorio ${name}`);
  }

  return brand;
}
