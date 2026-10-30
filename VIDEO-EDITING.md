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

## Trattamento immagine approvato — Ibrido Social Plus

Per ADV verticali ARPHÈ con una persona in camera, il riferimento approvato è un look caldo,
incisivo e adatto ai social, senza perdere la credibilità clinica della pelle. Il soggetto deve
separarsi chiaramente dallo sfondo, ma il trattamento non deve sembrare un filtro applicato.

Ordine di lavoro:

1. partire dalla sorgente nativa alla massima risoluzione disponibile; non usare Super Scale se
   il master 4K conserva già dettaglio sufficiente;
2. bilanciare esposizione e colore proteggendo pelle e alte luci;
3. applicare una presenza calda con contrasto e saturazione più decisi del look istituzionale;
4. in Fusion, separare il soggetto con una maschera verticale ampia e molto sfumata: lo sfondo
   può essere leggermente più scuro e meno saturo, senza alone visibile;
5. correggere patine, dominanti o fasce lattiginose solo localmente. La correzione deve essere
   limitata all'area difettosa e disattivata o animata quando volto, capelli o mani la attraversano;
6. controllare almeno un primo piano e un'inquadratura a figura intera prima della consegna.

Valori di partenza, da adattare caso per caso:

- temperatura complessiva circa `+0,14`;
- esposizione `-0,05`;
- contrasto complessivo circa `+0,28`;
- saturazione complessiva circa `1,12`;
- spotlight soggetto: centro indicativo `x=0,45`, `y=0,52`, larghezza `0,78`, altezza `1,16`,
  sfumatura `0,22`;
- sfondo dello spotlight: gain `0,90`, saturazione `0,92`.

Questi valori sono una base estetica, non un preset rigido. Evitare pelle plastificata, neri
chiusi, oversharpening, blur globale, gradienti percepibili, aloni attorno al soggetto e fasce
lucide o patinate sullo sfondo. Le correzioni devono passare da strumenti generici e riutilizzabili:
non creare mai comandi del bridge dedicati a un singolo video.

Risultato approvato il 30 ottobre 2026 sul test ADV verticale “Sguardo stanco”.

## Leggibilità Story/Reel

Nel canvas `1080x1920`, ogni elemento essenziale deve restare nel rettangolo sicuro compreso tra
`x=86..907` e `y=192..1574`. Il template HTML controlla Satoshi 400, 500 e 700 dopo
`document.fonts.ready`: se manca anche un solo peso mostra `DRAFT — FONT FALLBACK`.

Il fallback tecnico permette di aprire e correggere il template offline, ma non è una resa finale.
La consegna è finale solo quando il badge non compare e tutti i pesi richiesti risultano caricati.
