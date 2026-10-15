import { mkdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import process from 'node:process';
import { fileURLToPath } from 'node:url';

import { chromium } from 'playwright';
import { readOptionalAsset, resolveSafePath, SpecificationValidationError, validateSpecification } from './asset-validator.js';
import { loadBrand } from './brand-loader.js';
import { createInstagramPost, defaults as instagramDefaults } from './templates/instagram-post.js';
import { createYouTubeThumbnail, defaults as youtubeDefaults } from './templates/youtube-thumbnail.js';

export class RenderValidationError extends Error {
  constructor(message) {
    super(message);
    this.name = 'RenderValidationError';
  }
}

const rendererRootDefault = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const templates = {
  'youtube-thumbnail': { defaults: youtubeDefaults, compose: createYouTubeThumbnail },
  'instagram-post': { defaults: instagramDefaults, compose: createInstagramPost },
};

function fileFontSource(buffer) {
  return `url(data:font/ttf;base64,${buffer.toString('base64')})`;
}

function reportPathFor(output) {
  const extension = path.extname(output);
  return `${output.slice(0, -extension.length)}.report.json`;
}

function ensureDimensions(specification, defaults) {
  const width = specification.width ?? defaults.width;
  const height = specification.height ?? defaults.height;
  if (width !== defaults.width || height !== defaults.height) {
    throw new RenderValidationError(`il template ${specification.template} richiede ${defaults.width} × ${defaults.height}`);
  }
  return { width, height };
}

async function loadFontFaces(brand) {
  const titleContents = await readFile(brand.fonts.title.source.file);
  const fontFaces = [{
    family: brand.fonts.title.family,
    weight: brand.fonts.title.weight,
    style: brand.fonts.title.style,
    source: fileFontSource(titleContents),
    asset: brand.fonts.title.source.file,
  }];
  const configuredDirectory = process.env[brand.fonts.body.source.directoryEnvironment];
  const fontDirectory = configuredDirectory ?? path.join(process.env.WINDIR ?? '', 'Fonts');
  for (const weight of brand.fonts.body.weights) {
    const fontFile = brand.fonts.body.source.files?.[weight];
    const fontPath = fontFile && path.join(fontDirectory, fontFile);
    let contents;
    try {
      contents = await readFile(fontPath);
    } catch {
      throw new RenderValidationError(`font richiesto mancante: Satoshi peso ${weight} (${fontPath ?? 'file non configurato'})`);
    }
    fontFaces.push({
      family: brand.fonts.body.family,
      weight,
      style: 'normal',
      source: fileFontSource(contents),
      asset: fontPath,
    });
  }
  return fontFaces;
}

function makeBackground(asset) {
  if (!asset) return null;
  return { ...asset, extension: path.extname(asset.file).toLowerCase() };
}

export async function renderGraphic({ rendererRoot = rendererRootDefault, specification, specificationPath, brandOverrides } = {}) {
  validateSpecification(specification);
  const template = templates[specification.template];
  const dimensions = ensureDimensions(specification, template.defaults);
  const baseDirectory = specificationPath ? path.dirname(specificationPath) : rendererRoot;
  const brand = await loadBrand({ rendererRoot, overrides: brandOverrides });
  const output = resolveSafePath({ rendererRoot, baseDirectory, requestedPath: specification.output, label: 'output' });
  const background = makeBackground(await readOptionalAsset({ rendererRoot, baseDirectory, requestedPath: specification.background, label: 'background' }));
  const logo = await readOptionalAsset({ rendererRoot, requestedPath: path.relative(rendererRoot, brand.logos.ink.file), label: 'logo obbligatorio' });
  const fontFaces = await loadFontFaces(brand);
  const html = template.compose({ ...dimensions, title: specification.title, subtitle: specification.subtitle, colors: brand.colors, logo, background, fontFaces });

  const browser = await chromium.launch({ headless: true });
  try {
    const page = await browser.newPage({ viewport: dimensions, deviceScaleFactor: 1 });
    await page.setContent(html, { waitUntil: 'load' });
    await page.waitForFunction(() => window.__rendererReady === true, null, { timeout: 15000 });
    const fonts = await page.evaluate(() => window.__rendererFontResults);
    const unavailable = fonts.find((font) => !font.loaded);
    if (unavailable) throw new RenderValidationError(`font richiesto non caricato: ${unavailable.family} peso ${unavailable.weight}`);
    const overflow = await page.locator('[data-overflow]').evaluateAll((elements) => elements
      .map((element) => ({ name: element.dataset.overflow, vertical: element.scrollHeight - element.clientHeight, horizontal: element.scrollWidth - element.clientWidth }))
      .filter((entry) => entry.vertical > 1 || entry.horizontal > 1));
    if (overflow.length) throw new RenderValidationError(`testo non contenibile nel template: ${overflow.map((entry) => `${entry.name} (${entry.horizontal}px orizzontali, ${entry.vertical}px verticali)`).join(', ')}`);

    await mkdir(path.dirname(output), { recursive: true });
    await page.screenshot({ path: output, type: 'png' });
    const report = {
      brand: brand.brand,
      template: specification.template,
      dimensions,
      output,
      fonts: fonts.map(({ family, weight, style, loaded, status, asset }) => ({ family, weight, style, loaded, status, asset })),
      assets: { logo: brand.logos.ink.file, background: background?.file ?? null },
    };
    await writeFile(reportPathFor(output), `${JSON.stringify(report, null, 2)}\n`, 'utf8');
    return report;
  } finally {
    await browser.close();
  }
}

async function runCli() {
  const argumentIndex = process.argv.indexOf('--input');
  if (argumentIndex === -1 || !process.argv[argumentIndex + 1]) {
    throw new RenderValidationError('uso: npm run render -- --input percorso/spec.json');
  }
  const input = path.resolve(process.cwd(), process.argv[argumentIndex + 1]);
  const specification = JSON.parse(await readFile(input, 'utf8'));
  const report = await renderGraphic({ specification, specificationPath: input });
  process.stdout.write(`PNG creato: ${report.output}\nReport: ${reportPathFor(report.output)}\n`);
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  runCli().catch((error) => {
    process.stderr.write(`ERRORE RENDERER: ${error.message}\n`);
    process.exitCode = 1;
  });
}

export { SpecificationValidationError };
