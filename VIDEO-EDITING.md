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

## Sottotitoli Fusion ARPHÈ approvati

Il preset validato per ADV e Reel verticali usa un'unica frase visibile con avanzamento karaoke
parola per parola. La parola pronunciata riceve lo sfondo bordeaux; le altre restano bianche senza
sfondo.

- Font: **Satoshi Bold**, sempre maiuscolo.
- Parola in evidenza: **Satoshi Bold Italic**, al massimo una per frase.
- Misure Fusion ammesse: `0.050` standard e `0.065` evidenza. Non sono consentite misure
  intermedie o riduzioni dinamiche parola per parola.
- Lo sfondino usa il token bordeaux del kit, segue la larghezza della parola e conserva margini
  interni costanti.
- La frase occupa una riga quando entra nella safe area; altrimenti viene bilanciata su un massimo
  di due righe centrate.
- Se due righe non bastano, la frase viene separata in due gruppi temporali leggibili: il carattere
  non viene rimpicciolito.
- Spaziatura, allineamento e safe area devono restare costanti per tutto il video.

Questa resa è stata approvata il 31 ottobre 2026 sulla review verticale
`ARPHE_ADV_RICERCA_PERSONALE_REVIEW_V4_TWO_SIZES`. Il riferimento è estetico e generico: non deve
produrre comandi, preset o eccezioni dedicati a quel singolo video.
