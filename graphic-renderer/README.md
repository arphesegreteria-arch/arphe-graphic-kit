# Renderer grafico locale ARPHÈ

Questo strumento crea PNG social e thumbnail con il browser locale. Le fotografie o gli sfondi creativi restano file esterni; titoli, sottotitoli, colori e logo vengono composti in modo deterministico con le regole del Graphic Kit.

Non usa servizi cloud durante il rendering e non scarica font. Il rendering fallisce se manca un font o un logo richiesto: non usa fallback silenziosi.

## Installazione (Windows)

1. Installa Node.js LTS 22 o successivo da <https://nodejs.org/>.
2. Installa Satoshi Regular 400, Medium 500 e Bold 700 seguendo `../fonts/SATOSHI.md`. La licenza vieta di inserirne i file nel repository.
3. Apri PowerShell nella cartella `graphic-renderer` e avvia:

```powershell
npm ci
npx playwright install chromium
npm run check-environment
npm run validate-brand
```

Se i font Satoshi non sono nella cartella standard di Windows, imposta prima `ARPHE_SATOSHI_DIR` alla cartella che contiene `Satoshi-Regular.otf`, `Satoshi-Medium.otf` e `Satoshi-Bold.otf`:

```powershell
$env:ARPHE_SATOSHI_DIR = 'D:\Font autorizzati\Satoshi'
```

Questa variabile resta locale alla postazione e non va inserita nel repository.

## Creare una grafica

```powershell
npm run render -- --input examples/thumbnail.json
npm run render -- --input examples/instagram-post.json
```

Oppure fai doppio clic su `render.bat` da un prompt e passa `--input examples/thumbnail.json`.

Ogni JSON richiede `brand`, `template`, `title` e `output`; `subtitle` e `background` sono opzionali. I percorsi sono relativi al file JSON e devono restare nel repository.

```json
{
  "brand": "arphe",
  "template": "youtube-thumbnail",
  "title": "LA MEDICINA DEL FUTURO",
  "subtitle": "Scienza e innovazione",
  "background": "../assets/foto.png",
  "output": "../output/thumbnail.png"
}
```

Template disponibili:

- `youtube-thumbnail` — 1280 × 720
- `instagram-post` — 1080 × 1080

Le dimensioni sono fisse per template nella prima versione. I ritorni a capo sono supportati; se il testo non entra, il comando termina con un errore invece di ridurre automaticamente il font. Il file `output/<nome>.report.json` mostra i font e gli asset effettivamente utilizzati.

## Font e asset verificati

Il titolo usa il file incluso `fonts/noto-serif-display/NotoSerifDisplay-VariableFont_wdthwght.ttf`, peso 300. Sottotitoli e testo tecnico usano i file locali Satoshi 400, 500 e 700. Il renderer carica ogni faccia tramite l’API `FontFace` del browser, attende `document.fonts.ready` e blocca l’esportazione se una faccia non è effettivamente caricata.

Palette, loghi e percorsi canonici sono dichiarati in `brand.json`, con riferimenti alla fonte nel kit. `brand.json` è una rappresentazione derivata: non sostituisce `tokens/colors.json`, i loghi SVG o le linee guida.

## Test e manutenzione

```powershell
npm test
npm run validate-brand
```

I test controllano font e logo mancanti, testo italiano, overflow, dimensioni PNG e rendering dei due template. `output/` e `node_modules/` sono esclusi da Git.

Per aggiungere un template, crea un modulo in `src/templates/`, dichiara dimensioni e compositore in `src/render.js`, quindi aggiungi un test reale PNG. Mantieni le scelte di layout non espresse dal kit come proposte tecniche facilmente modificabili.

## Uso da parte di un agente AI

Un agente deve soltanto generare un JSON valido nel repository e invocare il comando locale:

```powershell
npm run render -- --input percorso/al-lavoro.json
```

L’agente non deve disegnare testo nello sfondo creativo né copiare font nel repository. Deve leggere l’eventuale errore di validazione e correggere il JSON o installare il font richiesto sulla postazione.

## Problemi comuni

- **`font richiesto mancante`**: installa Satoshi dal canale autorizzato o configura `ARPHE_SATOSHI_DIR`.
- **`logo obbligatorio mancante`**: ripristina il file originale del kit; non crearne una sostituzione.
- **`testo non contenibile`**: accorcia il copy, inserisci ritorni a capo o scegli un template diverso.
- **Chromium non trovato**: esegui `npx playwright install chromium`.
