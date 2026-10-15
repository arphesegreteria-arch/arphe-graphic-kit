import { dataUri, documentShell, escapeHtml } from './base.js';

export const defaults = { width: 1080, height: 1080 };

export function createInstagramPost({ width, height, title, subtitle, colors, logo, background, fontFaces }) {
  const backgroundCss = background ? `background-image: url("${dataUri(background.contents, background.extension)}");` : '';
  const css = `*{box-sizing:border-box}html,body{margin:0;width:${width}px;height:${height}px;overflow:hidden}.canvas{position:relative;width:${width}px;height:${height}px;background:${colors.cream};color:${colors.brown};font-family:"Satoshi",sans-serif}.photo{position:absolute;left:0;right:0;top:0;height:43%;background-position:center;background-size:cover;filter:grayscale(1);${backgroundCss}}.copy{position:absolute;left:74px;right:74px;bottom:72px;top:500px;display:flex;flex-direction:column}.accent{height:12px;width:124px;background:${colors.burgundy};margin-bottom:30px}.title{margin:0;max-height:350px;overflow:hidden;padding-block:4px;font-family:"Noto Serif Display ARPHE",serif;font-weight:300;font-size:86px;line-height:1.25;white-space:pre-wrap}.subtitle{margin:27px 0 0;max-height:108px;overflow:hidden;font-size:26px;line-height:1.35;font-weight:400;white-space:pre-wrap}.brand-logo{position:absolute;right:74px;top:52px;width:180px;height:auto;filter:none}`;
  return documentShell({ fontFaces, css, markup: `<main class="canvas"><div class="photo"></div><section class="copy"><div class="accent"></div><h1 class="title" data-overflow="title">${escapeHtml(title)}</h1>${subtitle ? `<p class="subtitle" data-overflow="subtitle">${escapeHtml(subtitle)}</p>` : ''}</section><img class="brand-logo" alt="ARPHÈ" src="${dataUri(logo.contents, '.svg')}"></main>` });
}
