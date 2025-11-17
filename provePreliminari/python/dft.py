from cmath import exp, pi
import numpy as np

def dft(segnale: list) -> np.ndarray:
    N = len(segnale)
    trasformata = [0 for _ in range(N)]

    for k in range(0, N):
        somma = complex(0)

        for n in range(0, N):
            somma += segnale[n] * exp(-1j * 2 * pi * n * k/N)

        trasformata[k] = somma

    return np.array(trasformata)

def shift(trasformata: np.ndarray) -> np.ndarray:
    N = len(trasformata)
    indice_centrale = int(N/2)

    if N % 2 == 0:
        vettore_finale = trasformata[indice_centrale:].tolist() + trasformata[:indice_centrale].tolist()
    else:
        vettore_finale = trasformata[:indice_centrale] + trasformata[indice_centrale:]

    return np.array(vettore_finale)