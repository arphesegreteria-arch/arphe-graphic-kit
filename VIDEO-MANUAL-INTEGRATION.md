# Collegamento con il Video Editing Manual

Il Graphic Kit e il manuale video restano due repository indipendenti:

```text
C:\ARPHE\
├── video-editing-manual\
└── arphe-graphic-kit\
```

## Uso manuale

- DaVinci Resolve importa loghi da `arphe-graphic-kit\logos\png\`.
- Canva importa logo, palette e template dalla clone locale di `arphe-graphic-kit`.
- Le regole editoriali e le procedure Resolve restano in `video-editing-manual`.

## Uso da automazioni future

Un'automazione può ricevere come configurazione un percorso locale dedicato, per esempio:

```text
C:\ARPHE\arphe-graphic-kit
```

Da lì può leggere `tokens/colors.json` e gli asset sotto `logos/`. Il percorso non deve essere
hardcoded nel codice e la sua introduzione nel bridge richiederà un'attività separata con test e
gate visivo. Questa repository non modifica il bridge.

## Versioni

Per lavori destinati alla pubblicazione, annotare il tag o commit del Graphic Kit usato. In questo
modo un video può essere rigenerato anche dopo un futuro aggiornamento della marca.
