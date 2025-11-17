Homework 1
===

Assegnato il 17 novembre, da consegnare l'8 dicembre in formato ZIP tramite la sezione elaborati del portale della didattica.

**Analisi in frequenza di brani musicali campionati usando FFT e DFT**

Si possono usare sia le versioni Matlab sia funzioni implementate da noi ad hoc. Seguiranno avvisi più dettagliati circa le modalità e le consegne.

## Consegna
Dobbiamo scegliere noi **due brani** di durata superiore ai **20 secondi** (non ci sono linee guida in merito, viene consigliato di scegliere caratteristiche un po' **diverse** a livello di **genere** per vedere delle differenze).

Dobbiamo stimare lo spettro di energia su **sotto-finestre** temporali di 0.5 oppure 1 secondo (più grandi non è detto che siano semplici da elaborare con il nostro hardware) tramite due approcci:

- calcolo esplicito della DFT (prodotto tra matrice e vettore, aka **algoritmo a mano** che va bene su segnali piccoli considerando la complessità)
- utilizzo della funzione di **libreria** FFT (su segnali complessi non è detto che dia lo stesso risultato, ma dovrebbero essere poco diversi l'uno dall'altro).

È nostro compito determinare la scala delle frequenze (valori e scala logaritmica/decimale).

## Materiale
Le canzoni sono scelte da noi, nelle slide sono presenti dei richiami teorici che ci serviranno. Sono anche presenti dei consigli tecnici. Anche se negli avvisi viene scritto tutto con Matlab nelle slide è presente Python (e la Bosco lo ha anche citato).

## Suggerimenti
Leggere la documentazione di audioread, fft e fftshift. Dobbiamo determinare noi quale **scala** sia migliore per i vari grafici (logaritmica o decimale).

Dobbiamo provare a *giocare* sulla durata delle finestre.

Nella relazione non è fondamentale inserire tutti i grafici, dobbiamo mettere solo quelli più significativi.

In questo caso la **frequenza di campionamento** è fissa perché dipende dal file in input, volendo possiamo provare a ridurla ma la Bosco consiglia di non farlo in generale ma solamente per fare delle osservazioni.

Le relazioni non devono essere dei *poemi*; vanno inseriti i risultati e i commenti. Volendo si possono analizzare più di 2 file per analizzarne i più significativi tra i due.