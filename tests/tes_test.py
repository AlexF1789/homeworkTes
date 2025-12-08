# questo file contiene alcuni unit test per assicurarsi che le funzioni implementate
# nel modulo TES funzionino senza problemi

# per il notebook finale non vengono considerati ma è comunque buona norma verificarne
# il funzionamento prima di ogni commit

import unittest, tes
import numpy as np
import math

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
        self.skipTest('Da valutarne la presenza')


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

    # test che prova a calcolare la funzione di trasferimento mediante il codice
    # e la verifica usando una funzione di trasferimento nota
    def test_funzione_trasferimento(self):
        # creiamo il segnale rumore
        durata = tes.get_durata_per_taglio(1_000, tes.Tipo_filtro.PORTA, 0)
        noise = np.random.randn(math.ceil(durata*44_100))

        # creiamo il filtro nel tempo
        porta = tes.get_porta_discreta(durata, 0, 44_100, math.ceil(durata*44_100))

        # calcoliamo l'uscita e la trasformata del filtro
        uscita = np.convolve(noise, porta)
        n_fft = uscita.size
        trasf_filtro = np.abs(np.fft.fftshift(np.fft.fft(porta, n=n_fft)))

        # calcoliamo le trasformate dell'ingresso e dell'uscita per calcolare
        noise_f = np.fft.fftshift(np.fft.fft(noise, n=n_fft))
        uscita_f = np.fft.fftshift(np.fft.fft(uscita, n=n_fft))

        funz_trasf = tes.calcola_funzione_trasferimento(noise_f, uscita_f)

        # verifichiamo che la funzione di trasferimento attesa corrisponda a quella calcolato
        self.assertTrue(
            np.allclose(
                funz_trasf,
                trasf_filtro,
                atol=0.01
            )
        )