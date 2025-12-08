import numpy as np
from cmath import exp, pi
import ctypes, platform, os

# calcola la dft del segnale in input adoperando
# interamente codice Python
#
# riceve il segnale (campioni) in input e ne
# restituisce la trasformata (valori complessi)
def dft_python(segnale: np.ndarray) -> np.ndarray:
    N = len(segnale)
    trasformata = [0 for _ in range(N)]

    for k in range(0, N):
        somma = complex(0)

        for n in range(0, N):
            somma += segnale[n] * exp(-1j * 2 * pi * n * k/N)

        trasformata[k] = somma

    return np.array(trasformata)

# Data una trasformata ne calcola lo spettro
# calcolando i quadrati di ogni coefficiente
def get_spettro(trasformata: np.ndarray) -> np.ndarray:
    return np.square(trasformata)

# Calcola la DFT di un segnale in input adoperando
# codice C che viene chiamato in maniera trasparente
#
# riceve il segnale (campioni) e restituisce la
# trasformata di cui è già stato calcolato il valore
# assoluto
def dft_c(segnale: np.ndarray) -> np.ndarray:
    file_oggetto_c = str(os.path.join('obj', 'dft'))

    # determiniamo a quale file oggetto linkare in base all'OS
    match platform.system():
        case 'Windows':
            file_oggetto_c += '.dll'
        case 'Linux':
            file_oggetto_c += '.so'
        case 'Darwin':
            file_oggetto_c += '.o'
        case _:
            raise Exception('Piattaforma non riconosciuta!')

    # registriamo la funzione in C
    lib = ctypes.cdll.LoadLibrary(file_oggetto_c)
    lib.dft.argtypes = (ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.c_int)
    lib.dft.restype = None

    # creiamo il puntatore a input e output
    ptr_input = segnale.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
    output = np.array([0 for _ in range(len(segnale))], dtype=np.float32)
    ptr_output = output.ctypes.data_as(ctypes.POINTER(ctypes.c_float))

    # chiamiamo la funzione in C e restituiamo il risultato
    lib.dft(ptr_input, ptr_output, len(segnale))

    return output

# Calcola la DFT di un segnale in input adoperando
# codice C che viene chiamato in maniera trasparente
# e che adopera computazione parallela
#
# riceve il segnale (campioni) e restituisce la
# trasformata di cui è già stato calcolato il valore
# assoluto
def dft_c_parallela(segnale: np.ndarray) -> np.ndarray:
    file_oggetto_c = str(os.path.join('obj', 'dftParallela'))

    # determiniamo a quale file oggetto linkare in base all'OS
    match platform.system():
        case 'Windows':
            file_oggetto_c += '.dll'
        case 'Linux':
            file_oggetto_c += '.so'
        case 'Darwin':
            file_oggetto_c += '.o'
        case _:
            raise Exception('Piattaforma non riconosciuta!')

    # registriamo le funzioni in C
    lib = ctypes.cdll.LoadLibrary(file_oggetto_c)
    lib.dft.argtypes = (ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.c_int)
    lib.dft.restype = None

    lib.getNumeroProcessori.restype = ctypes.c_int

    # creiamo il puntatore a input e output
    ptr_input = segnale.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
    output = np.array([0 for _ in range(len(segnale))], dtype=np.float32)
    ptr_output = output.ctypes.data_as(ctypes.POINTER(ctypes.c_float))

    # stampiamo il numero di processori in uso
    print(lib.getNumeroProcessori(), 'processori in uso...')

    # chiamiamo la funzione in C e restituiamo il risultato
    lib.dft(ptr_input, ptr_output, len(segnale))

    return output

# Effettua lo shift della fft del segnale
# scambiando le frequenze negative e positive rendendone
# dunque il grafico accurato
def shift(trasformata: np.ndarray) -> np.ndarray:
    N = len(trasformata)
    indice_centrale = int(N/2)

    if N % 2 != 0:
        indice_centrale += 1

    vettore_finale = trasformata[indice_centrale:].tolist() + trasformata[:indice_centrale].tolist()

    return np.array(vettore_finale)

# Restituisce la frequenza limite (positiva) che corrisponde
# alla banda al valore passato come parametro in percentuale
# della banda (di default il valore considerato è il 99%)
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