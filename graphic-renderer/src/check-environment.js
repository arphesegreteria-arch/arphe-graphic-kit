import { access } from 'node:fs/promises';
import path from 'node:path';

import { chromium } from 'playwright';
import { loadBrand } from './brand-loader.js';

async function main() {
  const brand = await loadBrand();
  const directory = process.env[brand.fonts.body.source.directoryEnvironment] ?? path.join(process.env.WINDIR ?? '', 'Fonts');
  for (const weight of brand.fonts.body.weights) await access(path.join(directory, brand.fonts.body.source.files[weight]));
  await access(chromium.executablePath());
  console.log(`Node.js ${process.version}: OK`);
  console.log(`Playwright Chromium: ${chromium.executablePath()}`);
  console.log(`Satoshi: ${directory}`);
  console.log('Ambiente renderer: OK');
}

main().catch((error) => {
  console.error(`AMBIENTE NON PRONTO: ${error.message}`);
  process.exitCode = 1;
});
