# file contenente eventuali funzioni di appoggio da non inserire direttamente
# nel notebook Python (analogamente a quanto fatto per l'homework 1)

import numpy as np
import matplotlib.pyplot as plt
import typing, math

# genera un filtro discreto e lo restituisce come vettore NumPy
#
# durata: durata del segnale filtro continuo in secondi
# traslazione: traslazione (espressa come positiva verso destra e negativa verso sinistra) del segnale filtro
# numero_campioni: indica il numero di campioni di cui deve essere composto il segnale discreto in uscita
# callable: indica la funzione che fornisce il valore del segnale del filtro continuo dato il tempo
#
# restituisce un vettore NumPy di dimensione numero_campioni
def get_filtro_discreto(durata: float, traslazione: float, frequenza_campionamento: float, numero_campioni: int, callable: typing.Callable[[float], float]) -> np.ndarray:
    if numero_campioni <= 0:
        raise Exception('Numero di campioni non valido!')
    
    if frequenza_campionamento <= 0:
        raise Exception('Frequenza di campionamento non valida!')

    vettore = np.zeros(numero_campioni)

    for i in range(numero_campioni):
        tempo_continuo = i * (1/frequenza_campionamento)

        if traslazione <= tempo_continuo <= durata+traslazione:
            vettore[i] = callable(tempo_continuo)

    return vettore

# genera un filtro discreto porta e lo restituisce come vettore NumPy
#
# durata: durata del segnale filtro continuo in secondi
# traslazione: traslazione (espressa come positiva verso destra e negativa verso sinistra) del segnale filtro
# numero_campioni: indica il numero di campioni di cui deve essere composto il segnale discreto in uscita
# callable: indica la funzione che fornisce il valore del segnale del filtro continuo dato il tempo
#
# restituisce un vettore NumPy di dimensione numero_campioni
def get_porta_discreta(durata: float, traslazione: float, frequenza_campionamento: float, numero_campioni: int):
    return get_filtro_discreto(durata, traslazione, frequenza_campionamento, numero_campioni, lambda _: 1)


# genera un filtro discreto coseno rialzato e lo restituisce come vettore NumPy
#
# durata: durata del segnale filtro continuo in secondi
# traslazione: traslazione (espressa come positiva verso destra e negativa verso sinistra) del segnale filtro
# numero_campioni: indica il numero di campioni di cui deve essere composto il segnale discreto in uscita
# callable: indica la funzione che fornisce il valore del segnale del filtro continuo dato il tempo
#
# restituisce un vettore NumPy di dimensione numero_campioni
def get_coseno_rialzato(durata: float, traslazione: float, frequenza_campionamento: float, numero_campioni: int, beta: float) -> np.ndarray:
    return get_filtro_discreto(durata, traslazione, frequenza_campionamento, numero_campioni, lambda x: calcola_funzione_coseno_rialzato(x, durata/2, beta))

# calcola il valore della funzione coseno rialzato dati i parametri
#
# x: valore nel quale vogliamo calcolare la funzione
# T: ampiezza del filtro (come da grafico)
# beta: parametro compreso tra 0 e 1
def calcola_funzione_coseno_rialzato(x: float, T: float, beta: float) -> float:
    if beta < 0 or beta > 1:
        raise Exception('Valore di beta non consentito!')

    soglia = T / (2*beta)

    if x == soglia or x == (-1 * soglia):
        return np.sinc(1 / (2*beta)) * math.pi / (4 * T)
    
    return (np.sinc(x/T) / T) * (math.cos(math.pi * beta * x / T) / (1 - (2*beta*x / T)**2))

# effettua la convoluzione di due segnali
#
# segnale1: è uno dei due segnali espresso come vettore NumPy
# segfnale2: è l'altro segnale espresso come vettore NumPy
#
# restituisce un vettore NumPy che ne rappresenta la convoluzione
def convoluzione(segnale1: np.ndarray, segnale2: np.ndarray) -> np.ndarray:
    dim_conv = segnale1.size + segnale2.size - 1
    risultato = np.zeros(dim_conv)

    for k in range(dim_conv):
        for n in range(max(0, k - segnale2.size + 1), min(k + 1, segnale1.size)):
            risultato[k] += segnale1[n] * segnale2[k-n]

    return risultato


# GRAFICI DI PROVA PER COSENO RIALZATO E SINC
#plt.stem([i for i in range(50)], get_coseno_rialzato(3, 0, 10, 50, 0.15))
#plt.stem([x for x in range(50)], get_filtro_discreto(10, 0, 10, 50, lambda x: np.sinc(x)))

# ones = np.ones(5)
# sones = np.ones(8)
# exit = np.convolve(ones, sones)
# print(exit, exit.size)

# plt.stem(exit)
# plt.xlim((-10, 110))
# plt.grid(True)
# plt.show()