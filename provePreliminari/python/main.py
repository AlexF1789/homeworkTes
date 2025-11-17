import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt

from dft import dft as custom_dft
from dft import shift as custom_shift

audio, _ = sf.read('prova.oga')
audio = audio[:, 0]

fourier = custom_shift(custom_dft(audio[:50]))
stock = np.fft.fftshift(np.fft.fft(audio, n=50))

for i in range(50):
    print(fourier[i], stock[i])

plt.stem(abs(fourier))
plt.grid(True)
plt.show()