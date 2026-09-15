# ARPHE Graphic Kit

Questa repository è la **fonte di verità grafica** di ARPHE. Contiene asset e regole utilizzabili
da un altro computer senza dipendere dalla macchina che ha creato il pacchetto.

> La fonte di verità operativa del montaggio resta
> [`video-editing-manual`](https://github.com/arphesegreteria-arch/video-editing-manual).
> Il Graphic Kit non modifica né configura automaticamente DaVinci Resolve o il bridge.

## Inizia da qui

| Se devi… | Apri… |
|---|---|
| impostare Canva | [`CANVA.md`](CANVA.md) |
| montare o creare grafiche video | [`VIDEO-EDITING.md`](VIDEO-EDITING.md) |
| collegarlo al manuale video | [`VIDEO-MANUAL-INTEGRATION.md`](VIDEO-MANUAL-INTEGRATION.md) |
| chiedere una grafica a un'AI | [`AI-USAGE.md`](AI-USAGE.md) |
| installare Satoshi | [`fonts/SATOSHI.md`](fonts/SATOSHI.md) |
| verificare licenze e provenienza | [`LICENSES.md`](LICENSES.md) |

## Cosa puoi estrarre

### Logo

Gli SVG in `logos/svg/` sono i master. Per Canva e software video sono disponibili PNG
trasparenti con lato lungo da 512, 1024, 2048 e 4096 pixel in due versioni:

- `ink`: `#1B170E`, per fondi chiari;
- `cream`: `#F8F4EE`, per fondi scuri.

Non ricolorare, ruotare, deformare o ricreare il logo con AI.

### Palette

La stessa palette è disponibile in:

- `tokens/colors.txt` — copia manuale in Canva;
- `tokens/colors.css` — siti e template HTML;
- `tokens/colors.json` — automazioni e strumenti software.

### Template

| Uso | Dimensione | HTML | SVG per Canva |
|---|---:|---|---|
| Post verticale | 1080×1350 | `templates/social/post-1080x1350.html` | `templates/social/post-1080x1350.svg` |
| Storia/Reel | 1080×1920 | `templates/social/story-1080x1920.html` | `templates/social/story-1080x1920.svg` |
| Titolo video 16:9 | 1920×1080 | `templates/video/title-card-1920x1080.html` | `templates/video/title-card-1920x1080.svg` |

Gli HTML mostrano il logo vero tramite un percorso relativo. Gli SVG sono autosufficienti e
mantengono il testo editabile, ma contengono un riquadro `INSERISCI LOGO`: dopo l'importazione in
Canva aggiungere il logo dalla cartella `logos/`.

## Regole essenziali

1. Titolo in Noto Serif Display 300, mai in grassetto.
2. Testo, etichette e bottoni in Satoshi.
3. Un solo elemento pieno bordeaux per grafica.
4. Fotografie in bianco e nero.
5. Angoli da 0 a 5 px; bottoni ad angoli vivi.
6. Niente gradienti, bagliori o ombre evidenti.

Le regole complete sono in `brand-guidelines/`.

## Limiti dichiarati

Satoshi non è incluso perché la sua licenza vieta la redistribuzione pubblica. Il fiore e la
fotografia dell'esempio ricevuto non sono inclusi perché non sono stati forniti come sorgenti
separati con provenienza documentata. Vedi `elements/README.md`.

## Verifica del kit

Da questa cartella:

```bash
python scripts/verify_kit.py
```

Risultato atteso: `ARPHE GRAPHIC KIT: PASS`.
