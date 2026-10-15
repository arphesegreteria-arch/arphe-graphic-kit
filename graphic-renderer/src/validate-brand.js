import { access } from 'node:fs/promises';
import path from 'node:path';

import { loadBrand } from './brand-loader.js';

async function main() {
  const brand = await loadBrand();
  const directory = process.env[brand.fonts.body.source.directoryEnvironment] ?? path.join(process.env.WINDIR ?? '', 'Fonts');
  for (const weight of brand.fonts.body.weights) {
    const font = path.join(directory, brand.fonts.body.source.files[weight]);
    try {
      await access(font);
    } catch {
      throw new Error(`font richiesto mancante: Satoshi peso ${weight} (${font})`);
    }
  }
  console.log(`Brand ${brand.brand}: OK`);
  console.log(`Noto Serif Display: ${brand.fonts.title.source.file}`);
  console.log(`Satoshi 400/500/700: ${directory}`);
  console.log(`Logo: ${brand.logos.ink.file}`);
}

main().catch((error) => {
  console.error(`ERRORE BRAND: ${error.message}`);
  process.exitCode = 1;
});
