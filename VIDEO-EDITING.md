# Uso nel montaggio video

## Formati

- `1920x1080`: master orizzontale 16:9.
- `1080x1920`: Reel, Story e Short verticale.
- `1080x1350`: post verticale; non è un formato video master.

## Loghi

Preferisci SVG quando il software lo supporta. In DaVinci Resolve usa i PNG trasparenti 2048 o
4096 per evitare problemi di compatibilità. Scegli `ink` su fondi chiari e `cream` su fondi scuri.

Non ingrandire il PNG 512 per un master 4K. Non applicare ombre, contorni, rotazioni o stiramenti.

## Flusso consigliato

1. Scegli il template della risoluzione della timeline.
2. Sostituisci il placeholder con una foto o clip desaturata.
3. Usa Noto Serif Display 300 per il titolo e Satoshi per testi e bottoni.
4. Mantieni un solo accento pieno bordeaux.
5. Esporta gli overlay con canale alfa oppure ricostruisci i componenti in Fusion usando i token.

Il Graphic Kit descrive la resa grafica. Le procedure operative e i gate di Resolve restano nei
documenti principali della repository.

## Leggibilità Story/Reel

Nel canvas `1080x1920`, ogni elemento essenziale deve restare nel rettangolo sicuro compreso tra
`x=86..907` e `y=192..1574`. Il template HTML controlla Satoshi 400, 500 e 700 dopo
`document.fonts.ready`: se manca anche un solo peso mostra `DRAFT — FONT FALLBACK`.

Il fallback tecnico permette di aprire e correggere il template offline, ma non è una resa finale.
La consegna è finale solo quando il badge non compare e tutti i pesi richiesti risultano caricati.
