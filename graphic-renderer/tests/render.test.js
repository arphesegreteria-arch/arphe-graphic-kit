import assert from 'node:assert/strict';
import { mkdir, mkdtemp, readFile, rm } from 'node:fs/promises';
import path from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

import { renderGraphic, RenderValidationError } from '../src/render.js';
import { readOptionalAsset, SpecificationValidationError, validateSpecification } from '../src/asset-validator.js';

const rendererRoot = fileURLToPath(new URL('..', import.meta.url));

async function pngDimensions(file) {
  const bytes = await readFile(file);
  return { width: bytes.readUInt32BE(16), height: bytes.readUInt32BE(20) };
}

async function renderExample(template, dimensions) {
  const outputRoot = path.join(rendererRoot, 'output');
  await mkdir(outputRoot, { recursive: true });
  const directory = await mkdtemp(path.join(outputRoot, 'test-'));
  const output = path.join(directory, `${template}.png`);
  try {
    const report = await renderGraphic({
      rendererRoot,
      specification: {
        brand: 'arphe', template, title: 'L’innovazione è già qui',
        subtitle: 'Scienza, cura e prevenzione', output,
      },
    });
    assert.deepEqual(await pngDimensions(output), dimensions);
    assert.equal(report.fonts.every((font) => font.loaded), true);
    assert.equal(report.assets.logo.endsWith('.svg'), true);
  } finally {
    await rm(directory, { recursive: true, force: true });
  }
}

test('renders the Italian YouTube thumbnail at 1280 × 720', async () => {
  await renderExample('youtube-thumbnail', { width: 1280, height: 720 });
});

test('renders the Italian Instagram post at 1080 × 1080', async () => {
  await renderExample('instagram-post', { width: 1080, height: 1080 });
});

test('rejects copy which exceeds a template text area', async () => {
  await assert.rejects(
    () => renderGraphic({
      rendererRoot,
      specification: {
        brand: 'arphe', template: 'youtube-thumbnail',
        title: 'Una frase intenzionalmente molto lunga '.repeat(80),
        output: path.join(rendererRoot, 'output', 'should-not-exist.png'),
      },
    }),
    (error) => error instanceof RenderValidationError && /non contenibile/i.test(error.message),
  );
});

test('rejects a missing Satoshi face rather than substituting a fallback', async () => {
  await assert.rejects(
    () => renderGraphic({
      rendererRoot,
      specification: { brand: 'arphe', template: 'instagram-post', title: 'Titolo', output: path.join(rendererRoot, 'output', 'should-not-exist.png') },
      brandOverrides: { fonts: { body: { source: { files: { 400: 'Satoshi-Definitely-Missing.otf' } } } } },
    }),
    (error) => error instanceof RenderValidationError && /Satoshi.*400/i.test(error.message),
  );
});

test('resolves relative output paths and repeats identical rendering byte-for-byte', async () => {
  const output = path.join(rendererRoot, 'output', 'repeatable.png');
  const report = path.join(rendererRoot, 'output', 'repeatable.report.json');
  try {
    const specification = {
      brand: 'arphe', template: 'youtube-thumbnail', title: 'MEDICINA DEL FUTURO',
      subtitle: 'Cura e innovazione', output: '../output/repeatable.png',
    };
    const specificationPath = path.join(rendererRoot, 'examples', 'relative-specification.json');
    await renderGraphic({ rendererRoot, specification, specificationPath });
    const first = await readFile(output);
    await renderGraphic({ rendererRoot, specification, specificationPath });
    assert.deepEqual(await readFile(output), first);
  } finally {
    await rm(output, { force: true });
    await rm(report, { force: true });
  }
});

test('rejects unknown specification keys instead of silently ignoring typos', () => {
  assert.throws(
    () => validateSpecification({ brand: 'arphe', template: 'youtube-thumbnail', title: 'Titolo', output: 'output/a.png', backgound: 'typo.png' }),
    (error) => error instanceof SpecificationValidationError && /chiavi non supportate/i.test(error.message),
  );
});

test('rejects a non-image background asset explicitly', async () => {
  await assert.rejects(
    () => readOptionalAsset({ rendererRoot, requestedPath: '../README.md', label: 'background' }),
    (error) => error instanceof SpecificationValidationError && /estensione non supportata/i.test(error.message),
  );
});
