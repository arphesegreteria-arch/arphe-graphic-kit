# Renderer grafico locale ARPHÈ Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Aggiungere un renderer CLI offline che produca PNG ARPHÈ con font e asset verificati.

**Architecture:** Un package Node in `graphic-renderer/` legge la configurazione derivata dal kit e le specifiche JSON, produce HTML locale e usa Playwright/Chromium per controllare font e overflow prima dello screenshot. Ogni template dichiara soltanto geometrie tecniche modificabili e usa i token originali.

**Tech Stack:** Node.js 22+, Playwright Chromium, HTML/CSS, SVG, JSON, Node test runner.

**Spec:** `docs/superpowers/specs/2026-10-16-local-graphic-renderer-design.md`

## Global Constraints

- Non modificare asset originali o usare percorsi assoluti e servizi remoti nel rendering.
- Palette, logo e Noto provengono esclusivamente dal kit; Satoshi è verificato come font di sistema e mai ridistribuito.
- Font, logo obbligatorio, asset e overflow producono errori espliciti, non fallback o riduzioni arbitrarie.
- PNG e report sono riproducibili e `output/` non è versionato.

## Review Focus

- Titolo con caratteri italiani e a capo esplicito: deve mantenere il testo senza overflow.
- Titolo oltre il limite: deve fallire prima dell'esportazione.
- Satoshi non installato o peso assente: deve fallire specificando famiglia e peso.
- Logo definito come obbligatorio ma assente: deve fallire prima dell'avvio browser.
- Background e output relativi: devono restare confinati a percorsi consentiti.

### Task 1: Scaffolding e contratto brand

**Files:** `graphic-renderer/package.json`, `.gitignore`, `brand.json`, `src/brand-loader.js`, `src/asset-validator.js`, `tests/brand-loader.test.js`.

- [ ] Scrivere test fallenti per palette, Noto, Satoshi e logo obbligatori.
- [ ] Eseguire test e confermare il fallimento per modulo assente.
- [ ] Implementare loader/validator con errori espliciti e percorsi relativi sicuri.
- [ ] Rieseguire test e confermare il passaggio.

### Task 2: Template e renderer CLI

**Files:** `src/templates/*.js`, `src/render.js`, `examples/*.json`, `tests/render.test.js`.

- [ ] Scrivere test fallenti per dimensioni, caratteri italiani, overflow e font mancanti.
- [ ] Eseguire test e confermare il fallimento.
- [ ] Implementare documenti HTML autosufficienti, attesa/controllo Font API, screenshot e report.
- [ ] Rieseguire test e confermare il passaggio.

### Task 3: Esperienza locale e prove finali

**Files:** `README.md`, `check-environment.js`, `render.bat`, output dimostrativi non tracciati.

- [ ] Scrivere test fallente per input relativo e report deterministico.
- [ ] Eseguire test e confermare il fallimento.
- [ ] Implementare comandi, istruzioni Windows e diagnostica ambiente.
- [ ] Eseguire suite, validazione brand, rendering dei due esempi e ispezione visiva dei PNG.
