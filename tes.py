# file contenente eventuali funzioni di appoggio da non inserire direttamente
# nel notebook Python (analogamente a quanto fatto per l'homework 1)

import numpy as np
import matplotlib.pyplot as plt
import typing, math
from enum import Enum
from scipy.optimize import brentq

class Tipo_filtro (Enum):
    PORTA = 1
    COS_RIALZATO = 2

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

def get_cr_passa_alto(durata: float, frequenza_campionamento : float, beta : float) -> np.ndarray:
    freqs = np.fft.fftfreq(int(durata*frequenza_campionamento), d=1/frequenza_campionamento)
    H_lp = np.array([trasformata_coseno_rialzato(f, durata/2, beta) for f in freqs])

    H_hp = 1 - H_lp

    h_hp = np.fft.fftshift(np.fft.ifft(H_hp))
    return np.real(h_hp)

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


# calcola la lunghezza nel tempo che il filtro deve avere per avere la frequenza di taglio richiesta
#
# f_taglio: frequenza di taglio desiderata
# tipo_filtro: tipo di filtro scelto
# beta: parametro per filtro di tipo "coseno rialzato"
def get_durata_per_taglio(f_taglio : float, tipo_filtro : Tipo_filtro, beta : float) -> float:
    #in scala lineare un riduzione di 3dB corrisponde a raggiungere il valore 1/sqrt(2)
    target = 1/np.sqrt(2)
    x_sol = 0
    if tipo_filtro == Tipo_filtro.PORTA:
        def f_da_risolvere_porta(x):
            return np.abs(np.sinc(x)) - target

        #usiamo la funzione brentq che risolve in maniera numerica ed efficace
        #l'equazione f(x) = 0, sappiamo che il risultato si trova circa intorno a 0.443
        x_sol = brentq(f_da_risolvere_porta, 0, 1)
    elif tipo_filtro == Tipo_filtro.COS_RIALZATO:
        def f_da_risolvere_cos(x):
            return trasformata_coseno_rialzato_b(x, beta) - target
        
        x_sol = brentq(f_da_risolvere_cos, 0, 1)

    return x_sol / f_taglio

def trasformata_coseno_rialzato_b(x, b):
        # x è |f|*T
        if x <= (1 - b) / 2:
            return 1.0
        elif x <= (1 + b) / 2:
            arg = (np.pi / b) * (x - (1 - b) / 2)
            return 0.5 * (1 + np.cos(arg))
        else:
            return 0.0

def trasformata_coseno_rialzato(f, T, b) -> float:
    soglia_inf = (1-b) / (2*T)
    soglia_sup = (1+b) / (2*T)

    if np.abs(f) <= soglia_inf:
        return 1.0
    elif soglia_inf < np.abs(f) <= soglia_sup:
        return 0.5 * (1+np.cos((np.pi*T)/b * (abs(f)-(1-b)/(2*T))))
    
    return 0.0
  
# Calcola la funzione di trasferimento del filtro dato un segnale in ingresso e la relativa uscita
#
# ingresso: è il vettore che rappresenta il segnale in ingresso (nel dominio della frequenza)
# uscita: è il vettore che rappresenta il segnale in uscita (nel dominio della frequenza)
#
# restituisce un vettore che rappresenta il valore assoluto della funzione di trasferimento
# calcolata nella frequenza corrispondente
def calcola_funzione_trasferimento(ingresso:np.ndarray, uscita: np.ndarray) -> np.ndarray:
    funz_trasf = np.zeros(ingresso.size)
    
    for f in range(ingresso.size):
        funz_trasf[f] = np.abs(uscita[f]) / np.abs(ingresso[f])
    
    return funz_trasf
  
  
def get_limite_banda(spettro: np.ndarray, Df: float, percentuale: int = 99) -> float:
    N = len(spettro)
    indice_centrale = N // 2 + 1

    energia_soglia = percentuale/100 * float(np.sum(spettro[:indice_centrale]))

    if energia_soglia == 0.0:
        return 0.0
    
    somma_cumulata = 0
    for i in range(indice_centrale):
        somma_cumulata += spettro[i]
        
        if somma_cumulata >= energia_soglia:
            return i * Df
    
    return (indice_centrale - 1) * Df

def get_spettro(trasformata: np.ndarray) -> np.ndarray:
    return np.square(trasformata)