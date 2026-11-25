# Uso nel montaggio video

## Grafia del marchio

La grafia corretta è **Arphé**, oppure **ARPHÉ** nei testi tutti maiuscoli. La e finale ha sempre l’**accento acuto**, anche in corsivo: `é` (Unicode U+00E9), `É` (Unicode U+00C9). Non usare l’accento grave `è`/`È`, il circonflesso, un apostrofo al posto dell’accento o una lettera non accentata nel testo visibile. Normalizzare i cue in Unicode NFC e verificare il carattere prima del render.

La regola deriva dalla grafia presente nelle istruzioni ufficiali `brand-guidelines/ISTRUZIONI-PER-AI.md`. Se documenti storici o precedenti cue riportano ARPHÈ, prevale questa grafia corretta. I nomi tecnici ASCII di file, cartelle, progetti e tool restano invariati. La correzione del marchio appartiene ai dati editoriali e alla documentazione; non aggiungere sostituzioni dedicate al marchio nel codice del bridge.

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

## Sottotitoli Fusion ARPHÉ approvati

Il preset validato per ADV e Reel verticali usa un'unica frase visibile con avanzamento karaoke
parola per parola. La parola pronunciata riceve lo sfondo bordeaux; le altre restano bianche senza
sfondo.

- Font: **Satoshi Bold**, sempre maiuscolo.
- Parola in evidenza: **Satoshi Bold Italic**, al massimo una per frase.
- Testo bianco con **contorno esterno scuro sottile**, sia standard sia in evidenza. Su Text+
  usare l'elemento di shading 2 in modalità Outline e Outside Only, colore inchiostro
  `#1B170E`, Thickness `0.018` e alpha `0.75`. Verificare la leggibilità su una zona chiara
  del girato e che il bordo lasci leggibili gli spazi tra le lettere.
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

## Raffinamento generale dell’11 novembre 2026

Su richiesta dell’utente, il karaoke usa parole più vicine e card aderenti: padding orizzontale complessivo `0.012`, distanza fra card `0.004`. Font, misure `0.050`/`0.065`, colori e timing restano quelli del kit. La separazione stimata fra gli estremi del testo è `0.016`, sopra il minimo `0.014`. Verificare anche i glifi reali nelle catture native.

Per un punch in progressivo su un cue, riusare `CAMERA_ZOOM` con punti frame/scala nei dati del piano: ingresso breve con easing e mantenimento della nuova inquadratura. Un avvicinamento distribuito su tutta la chiusura può essere troppo poco percepibile per questa richiesta. Nessun nuovo codice motion, comando o riferimento a un progetto nel bridge.

## Interlinea karaoke compatta

Raffinamento generale richiesto l’11 novembre 2026: avvicinare anche le due righe. In posizione LOWER, distanza fra i centri delle righe `0.060` e altezza card `0.050`; in UPPER `0.055`/`0.045`. Resta uno spazio verticale libero di `0.010` tra i rettangoli delle card (19,2px su1920px). Il testo mantiene font, grandezze, larghezze e timing approvati. Le card a riga singola mantengono altezza e posizione precedenti.

La funzione generale restituisce `card_height` per parola e il grafo Fusion usa quel valore nella maschera. Non ridurre la sola distanza fra righe lasciando card alte: verificare entrambi i fondi attivi, accenti e corsivi nelle catture native. Nessun riferimento al progetto nel bridge. Patch/test in `reference/patches/2026-11-11-caption-line-spacing/`.

## Gerarchia visiva per ADV e Reel

Il volto e la voce restano il riferimento principale. Gli inserti devono chiarire il contenuto,
non competere con il relatore.

- L'A-roll mantiene il trattamento colore ARPHÉ approvato e un incarnato naturale.
- I B-roll fotografici sono in bianco e nero, puliti, senza testo, watermark, split-screen o
  prima/dopo promozionali.
- Un B-roll a pieno schermo è ammesso quando copre intenzionalmente l'immagine ma conserva la voce.
  Quando è importante continuare a vedere il relatore, preferire una card laterale o un inserto più
  breve.
- Se un filmato esterno non è fluido anche nel render, sostituirlo con una still verticale ad alta
  qualità; non conservare un movimento difettoso soltanto per avere “più dinamismo”.
- Ingresso e uscita seguono parole precise della trascrizione. Un'immagine pertinente ma fuori tempo
  non è un inserto approvato.

## Prima comparsa del medico — nome e qualifica

Inserire il titolo di presentazione una volta, alla prima inquadratura utile in cui il medico
è riconoscibile nel montaggio definitivo. In apertura, agganciarlo al primo fotogramma utile
dopo il taglio iniziale. Usare due righe allineate a sinistra, con nome e qualifica verificati.
Esempio approvato: *Dr.ssa Alati* sulla prima riga e *Medico estetico* sulla seconda.

| Elemento | Specifica del riferimento verticale 1080 × 1920 |
| --- | --- |
| Nome | Satoshi **Bold Italic 700**, 68 px, con maiuscole e minuscole come nel nome. |
| Qualifica | Satoshi **Regular Italic 400**, 39 px, con maiuscola iniziale. |
| Colore e fondo | Testo avorio `#F7F2E8` su fondo trasparente, con il video visibile dietro il titolo. |
| Ombra | Nero al 47% di opacità, offset verso destra e in basso di `(3, 4)` px sul nome e `(2, 3)` px sulla qualifica. |
| Posizione | Metà inferiore a sinistra. Origini di disegno dall'angolo in alto a sinistra a `(78, 1110)` px per il nome e `(78, 1196)` px per la qualifica. |
| Durata e movimento | 2,5 s complessivi (75 frame a 30 fps), con dissolvenza in entrata di 5 frame e in uscita di 7 frame. |

Per risoluzioni proporzionali, scalare le misure dal riferimento. Adattare la posizione
all’inquadratura quando serve a lasciare liberi volto, sottotitoli karaoke e area delle
interfacce social. Verificare entrambe le varianti Italic di [Satoshi](fonts/SATOSHI.md)
sulla postazione e controllare la leggibilità sul filmato reale a titolo pienamente visibile.
In Resolve, usare una traccia grafica separata. Il riferimento è un overlay ProRes 4444
con canale alpha, sovrapposto all'A-roll.

## Card tematiche e chiarezza del contenuto

Una card tematica può tradurre in linguaggio immediato un concetto espresso nel parlato con un
termine tecnico. Il sottotitolo rimane fedele alla voce; la card ha funzione editoriale separata.

- Testo breve, maiuscolo, Satoshi Bold.
- Colori esclusivamente dal kit; bordeaux pieno usato come unico accento dominante.
- Un solo messaggio primario alla volta, dentro la safe area e senza coprire il viso.
- Controllare entrata, centro e uscita: nessuna lettera può venire tagliata durante l'animazione.
- Non duplicare nello stesso momento la stessa frase in card e sottotitolo.
- Non creare comandi bridge, preset o eccezioni dedicati alla frase mostrata.

## Verifica visiva minima

Prima della review controllare almeno apertura, metà e chiusura, entrambe le configurazioni dei
sottotitoli (una e due righe), tutte le parole enfatizzate, i B-roll e gli estremi temporali delle
card. Le catture native verificano composizione e margini; fluidità e audio si verificano sul
render.

La procedura operativa completa per la segreteria è in
`video-editing-manual/docs/17_ARPHE_SECRETARY_EDITING_WORKFLOW.md`.

