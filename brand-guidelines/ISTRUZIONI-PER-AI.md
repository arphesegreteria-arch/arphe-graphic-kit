# Arphé — istruzioni di marca per un'intelligenza artificiale

Questo file si **allega o si incolla** in una conversazione con un'AI (Claude, ChatGPT,
Gemini) prima di chiederle una grafica. Contiene tutto quello che serve per restare Arphé.

Copia da qui in giù.

---

## Chi è Arphé

Poliambulatorio privato a Brescia, Via Rodi 49. Medicina estetica, medicina dello sport e
riabilitazione, medicina specialistica. Il tono è **elegante e rassicurante, mai ostentato**:
un ambulatorio che assomiglia a una casa, non a una clinica.

## Colori — usa esattamente questi

| Nome | Codice | Uso |
|---|---|---|
| Crema | `#F8F4EE` | Il fondo di quasi tutto |
| Marrone | `#614432` | Titoli, testo, filetti |
| Bordeaux | `#680C09` | I bottoni. È **l'accento**: un solo elemento pieno per grafica |
| Rosso | `#8D0511` | Numeri e filetti degli elenchi |
| Inchiostro | `#1B170E` | Il nero del logo, per il testo su fondo chiaro |

**Non inventare altri colori.** Non usare blu, verdi, viola, oro, pastelli. Non usare
gradienti. Se serve un altro tono, usa una trasparenza di uno di questi cinque.

## Caratteri

- **Titoli: Noto Serif Display, peso 300.** Grande e sottile.
- **Testo, bottoni, etichette: Satoshi.** 400 per il testo corrente, 500 per le etichette,
  700 solo per i bottoni.

**Regola inderogabile: un titolo in grassetto non è Arphé.** L'eleganza sta nel contrasto fra
un carattere grande e un tratto sottile. Per dare enfasi a una parola si usa il *corsivo*,
mai il grassetto e mai un colore diverso.

Se i due caratteri non sono disponibili, i sostituti più vicini sono **Playfair Display**
(al posto del serif, sempre nel peso più leggero) e **DM Sans** (al posto di Satoshi).

## Forme

- Angoli **da 0 a 5px**. I bottoni non hanno angoli arrotondati affatto.
  Un raggio da 12-16px sposta il marchio in un'altra categoria: non farlo.
- **Niente ombre in rilievo, niente gradienti, niente bagliori.** L'unica ombra ammessa è un
  alone quasi invisibile: `0 0 20px` di marrone al 4%.
- **Niente veli o sfumature sopra le foto.** Le immagini corrono pulite.
- Molto spazio bianco attorno ai titoli.

## Fotografia

**Le foto di Arphé sono in bianco e nero.** Non è un filtro occasionale: è la regola.
Se generi o scegli un'immagine, desaturala. L'unico elemento a colori del marchio è un
fiore rosso, usato con parsimonia.

## Componenti

**Bottone** — fondo `#680C09`, testo bianco, MAIUSCOLO, peso 700, spaziatura fra le lettere
circa 1,5px, imbottitura circa 15px per 46px, **angoli vivi**.

**Etichetta del professionista** — scheda color crema, angoli 4px, con una **barretta
bordeaux verticale di 3px sul lato sinistro**. Dentro: il nome in serif peso 300 marrone, e
sotto la qualifica in Satoshi 500, maiuscolo, spaziato, più piccola.

**Elenco numerato** — numero in serif peso 300 rosso `#8D0511`, grande; accanto il titolo in
maiuscolo peso 700; sotto un **filetto rosso di 3px con un pallino pieno all'estremità
sinistra**. Il pallino è piccolo ma è quello che rende la riga riconoscibile: non ometterlo.

## Il logo

Il file va inserito, non ridisegnato. **Non chiedere a un'AI di generare il logo Arphé**:
qualsiasi cosa produca sarà sbagliata. Usa i file forniti.
Il logo non si ricolora, non si ruota, non si allunga, non si mette in un riquadro, e non
si circonda di contorni per renderlo leggibile: se non si legge, si sposta o si cambia sfondo.

## Le tre cose che si vedono subito, se sbagliate

1. **Il titolo è sottile** — peso 300, mai bold.
2. **Un solo bordeaux pieno** per grafica.
3. **Le foto in bianco e nero.**

Il resto sono sfumature.

## Vincolo di legge — questo viene prima dell'estetica

Arphé è una **struttura sanitaria**. In Italia la comunicazione sanitaria dev'essere
informativa, senza elementi promozionali o suggestivi (L. 145/2018).

**Non scrivere mai**: promesse o garanzie di risultato; percentuali di efficacia usate come
argomento di vendita; sconti, promozioni, offerte a tempo, "posti limitati"; prima/dopo come
dimostrazione di efficacia; testimonianze di pazienti sulle prestazioni; toni che inducono un
bisogno estetico o creano ansia.

**Si può dire**: che cos'è una prestazione e a chi si rivolge; come si svolge; le
controindicazioni; i titoli e le competenze dei professionisti; gli ambienti, la
strumentazione, l'organizzazione, gli orari.

I titoli si scrivono esatti: "medico specializzando" e "medico specialista" non sono
la stessa cosa.

## Come chiedermi una grafica

Quando ti chiedo una grafica, **producila in HTML e CSS** alla misura richiesta (per esempio
1080×1350 per un post), non come immagine generata: così i colori e i caratteri restano
esattamente questi. Poi la trasformo in immagine io.

Metti sempre in cima al foglio di stile la regola della pagina, con la stessa misura della
grafica, per esempio:

```css
@page { size: 1080px 1350px; margin: 0 }
html, body { margin: 0 }
```

Serve perché io possa stamparla in PDF dal browser e ottenere una pagina esattamente di
quella misura, senza margini bianchi. Il PDF poi lo carico su Canva e resta modificabile.

Per la stessa ragione il testo deve restare **testo vero**: niente parole disegnate come
immagini, niente testo dentro uno sfondo generato, niente `background-image` con parole
dentro. Solo così su Canva posso ancora correggerlo.

Se invece devo generare una fotografia, ricordati che va **in bianco e nero** e senza testo
sopra: il testo lo aggiungo dopo.
