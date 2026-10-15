export function escapeHtml(value) {
  return value.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;').replaceAll("'", '&#39;');
}

export function dataUri(contents, extension) {
  const mediaType = extension === '.svg' ? 'image/svg+xml' : extension === '.png' ? 'image/png' : extension === '.webp' ? 'image/webp' : 'image/jpeg';
  return `data:${mediaType};base64,${contents.toString('base64')}`;
}

export function documentShell({ css, markup, fontFaces }) {
  return `<!doctype html><html lang="it"><head><meta charset="utf-8"><style>${css}</style></head><body>${markup}<script>
window.__rendererFontResults = [];
window.__rendererReady = false;
(async () => {
  for (const spec of ${JSON.stringify(fontFaces)}) {
    try {
      const face = new FontFace(spec.family, spec.source, { weight: String(spec.weight), style: spec.style || 'normal' });
      await face.load();
      document.fonts.add(face);
      const checked = document.fonts.check(String(spec.weight) + ' 1em "' + spec.family + '"');
      window.__rendererFontResults.push({ ...spec, loaded: face.status === 'loaded' && checked, status: face.status });
    } catch (error) {
      window.__rendererFontResults.push({ ...spec, loaded: false, status: 'error', error: String(error) });
    }
  }
  await document.fonts.ready;
  window.__rendererReady = true;
})();
</script></body></html>`;
}
