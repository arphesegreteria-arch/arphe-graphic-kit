import assert from 'node:assert/strict';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

import { BrandValidationError, loadBrand } from '../src/brand-loader.js';

const rendererRoot = fileURLToPath(new URL('..', import.meta.url));

test('loads the ARPHÈ palette, original Noto font, and canonical logo', async () => {
  const brand = await loadBrand({ rendererRoot });

  assert.equal(brand.colors.cream, '#F8F4EE');
  assert.equal(brand.fonts.title.family, 'Noto Serif Display ARPHE');
  assert.equal(brand.fonts.title.source.kind, 'file');
  assert.equal(brand.logos.ink.required, true);
});

test('rejects a required logo that is missing', async () => {
  await assert.rejects(
    () => loadBrand({ rendererRoot, overrides: { logos: { ink: { file: 'logos/svg/missing.svg' } } } }),
    (error) => error instanceof BrandValidationError && /logo obbligatorio/i.test(error.message),
  );
});

test('rejects a required original font file that is missing', async () => {
  await assert.rejects(
    () => loadBrand({ rendererRoot, overrides: { fonts: { title: { source: { file: 'fonts/missing.ttf' } } } } }),
    (error) => error instanceof BrandValidationError && /font/i.test(error.message),
  );
});

test('rejects a brand asset path outside the repository', async () => {
  await assert.rejects(
    () => loadBrand({ rendererRoot, overrides: { fonts: { title: { source: { file: '../../../../../../Windows/win.ini' } } } } }),
    (error) => error instanceof BrandValidationError && /esce dal repository/i.test(error.message),
  );
});
