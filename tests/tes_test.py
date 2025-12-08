# questo file contiene alcuni unit test per assicurarsi che le funzioni implementate
# nel modulo TES funzionino senza problemi

# per il notebook finale non vengono considerati ma è comunque buona norma verificarne
# il funzionamento prima di ogni commit

import unittest, tes
import numpy as np

import matplotlib.pyplot as plt

class TesTests(unittest.TestCase):

    # test che prova la porta discreta nel tempo adoperando alcuni esempi
    # effettuati a mano
    def test_porta_tempo(self):
        porta_1 = tes.get_porta_discreta(
            durata = 2.5,
            traslazione = 1.25,
            frequenza_campionamento = 1, # effettuiamo un campione al secondo
            numero_campioni = 10
        )

        porta_05 = tes.get_porta_discreta(
            durata = 2.5,
            traslazione = 1.25,
            frequenza_campionamento = 2, # effettuiamo un campione ogni 0.5 secondi
            numero_campioni = 10
        )

        porta_2 = tes.get_porta_discreta(
            durata = 2.5,
            traslazione = 1.25,
            frequenza_campionamento = 0.5, # effettuiamo un campione ogni 2 secondi
            numero_campioni = 3
        )

        self.assertEqual(porta_1.tolist(), [0, 0, 1, 1, 0, 0, 0, 0, 0, 0])
        self.assertEqual(porta_05.tolist(), [0, 0, 0, 1, 1, 1, 1, 1, 0, 0])
        self.assertEqual(porta_2.tolist(), [0, 1, 0])

        self.assertRaises(Exception, tes.get_porta_discreta, 0, 0, 1, 0)
        self.assertRaises(Exception, tes.get_porta_discreta, 0, 0, 0, 1)
        self.assertRaises(Exception, tes.get_porta_discreta, 0, 0, 0, 0)

    # test che prova il coseno rialzato in frequenza adoperando alcuni esempi
    # effettuati a mano
    def test_coseno_rialzato(self):
        durata = 1_000
        traslazione = 0
        freq_camp = 1_000
        num_campioni = 500_000
        beta = 0.5
        T = durata / 2

        filtro_tempo = tes.get_coseno_rialzato(durata, traslazione, freq_camp, num_campioni, beta)
        trasf_numerica = np.fft.fft(filtro_tempo)
        magn_trasf_numerica = np.abs(trasf_numerica)[:num_campioni // 2] / num_campioni * T

        frequenze = np.fft.fftfreq(num_campioni, d=1/freq_camp)[:num_campioni // 2]
        trasf_def = np.abs(np.array([tes.trasf_cos_rialz(f, T, beta) for f in frequenze]))

        trasf_def *=  (magn_trasf_numerica[0] / trasf_def[0])

        plt.stem(trasf_def[:15], 'r1')
        plt.stem(magn_trasf_numerica[:15], 'c1')
        plt.show()

        self.assertTrue(np.allclose(magn_trasf_numerica, trasf_def, atol=0.001))


    # test che prova la porta discreta in frequenza adoperando alcuni esempi
    # effettuati a mano
    def test_porta_frequenza(self):
        self.skipTest("Non implementato")

    # test che prova la convoluzione scritta a mano rispetto a quella di libreria
    def test_conv(self):
        sgn1 = np.ones(50)
        sgn2 = np.ones(30)
        sgn3 = np.random.randn(25)

        self.assertEqual(
            np.round(np.convolve(sgn1, sgn2), 2).tolist(),
            np.round(tes.convoluzione(sgn1, sgn2), 2).tolist()
        )

        self.assertEqual(
            np.round(np.convolve(sgn1, sgn3), 2).tolist(),
            np.round(tes.convoluzione(sgn1, sgn3), 2).tolist()
        )

        self.assertEqual(
            np.round(np.convolve(sgn2, sgn3), 2).tolist(),
            np.round(tes.convoluzione(sgn2, sgn3), 2).tolist()
        )