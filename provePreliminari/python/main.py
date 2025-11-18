import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
import ctypes

from dft import dft as custom_dft
from dft import shift as custom_shift

audio, fs = sf.read('prova.oga')
audio = np.array(audio[:, 0], dtype=np.float32)

print("Lavoro su:", len(audio), "campionati a", fs/1000, "kHz")

#fourier = custom_shift(custom_dft(audio[:10_000]))
#stock = np.fft.fftshift(np.fft.fft(audio, n=50))

# for i in range(50):
#     print(fourier[i], stock[i])

audio = audio[:10_000]

lib = ctypes.cdll.LoadLibrary('./dft.dll')
lib.dft.argtypes = (ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.c_int)
lib.dft.restype = None

ptr_input = audio.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
output = np.array([0 for _ in range(len(audio))], dtype=np.float32)

ptr_output = output.ctypes.data_as(ctypes.POINTER(ctypes.c_float))

lib.dft(ptr_input, ptr_output, len(audio))

print(output)
plt.stem(abs(output))
plt.grid(True)
plt.show()