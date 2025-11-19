import numpy as np
from cmath import exp, pi
import ctypes, platform, os

# calcola la dft del segnale in input adoperando interamente
# codice Python
def dft_python(segnale: np.ndarray) -> np.ndarray:
    N = len(segnale)
    trasformata = [0 for _ in range(N)]

    for k in range(0, N):
        somma = complex(0)

        for n in range(0, N):
            somma += segnale[n] * exp(-1j * 2 * pi * n * k/N)

        trasformata[k] = somma

    return np.array(trasformata)

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

# effettua lo shift della fft del segnale
def shift(trasformata: np.ndarray) -> np.ndarray:
    N = len(trasformata)
    indice_centrale = int(N/2)

    if N % 2 != 0:
        indice_centrale += 1

    vettore_finale = trasformata[indice_centrale:].tolist() + trasformata[:indice_centrale].tolist()

    return np.array(vettore_finale)