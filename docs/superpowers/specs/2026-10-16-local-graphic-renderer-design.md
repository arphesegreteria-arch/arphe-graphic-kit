# Renderer grafico locale ARPHÈ — design

## Obiettivo

Integrare nel graphic kit un renderer locale e riproducibile che separi lo sfondo creativo dalla composizione deterministica di testi, loghi e colori ARPHÈ. Un lavoro è descritto da JSON e viene esportato in PNG da Chromium offline dopo l'installazione delle dipendenze.

## Fonte di verità e font

Il renderer legge palette da `tokens/colors.json`, loghi da `logos/svg/` e il font dei titoli dal file Noto Serif Display incluso. Le regole tipografiche provengono da `brand-guidelines/typography.md`.

Satoshi è un requisito per testo secondario, etichette e bottoni, ma non può essere inserito nel repository: la licenza ITF Free Font License ne vieta la redistribuzione. Il renderer lo richiede come font di sistema con `local("Satoshi")`, verifica nel browser i pesi 400, 500 e 700 e fallisce se uno manca. Non esistono fallback silenziosi.

## Componenti

- `brand.json`: configurazione derivata e tracciabile verso i file canonici del kit; contiene solo percorsi relativi e regole presenti nei documenti.
- `brand-loader.js`: legge e valida configurazione, asset e descrittori dei font.
- `asset-validator.js`: valida input JSON e risolve in modo confinato percorsi relativi a repository e specifica.
- `templates/`: due compositori HTML/CSS, YouTube 1280×720 e Instagram 1080×1080. Le scelte geometriche non previste dal kit sono dichiarate come proposte tecniche modificabili.
- `render.js`: CLI che esegue validazione, attende `document.fonts.ready`, verifica ogni faccia con `document.fonts.check`, rileva overflow, crea PNG e report JSON con asset/font effettivamente usati.

## Flusso e errori

1. La CLI legge una specifica JSON e valida chiavi, template e dimensioni.
2. Il loader verifica i file di brand obbligatori.
3. Il renderer incorpora localmente gli asset autorizzati nel documento HTML; non usa rete.
4. Chromium carica le facce font, espone stato e misure di overflow alla CLI.
5. Il renderer interrompe con errore esplicito per font, logo, sfondo, input o testo non contenibile mancanti.
6. Solo dopo i controlli salva PNG e `<nome>.report.json`.

## Verifica

Test Node verificano loader, font mancante, logo mancante, percorso relativo, overflow, dimensioni PNG, italiano e determinismo. Test di integrazione usano Chromium Playwright e generano output dimostrativi in `graphic-renderer/output/`, esclusa da Git.

## Portabilità

Il renderer richiede Node.js 22 LTS o successivo compatibile, `npm ci`, `npx playwright install chromium`, Chrome/Chromium fornito da Playwright e installazione individuale e autorizzata di Satoshi. Non usa percorsi assoluti, credenziali o servizi remoti durante il rendering.
