# questo file contiene alcuni unit test per assicurarsi che le funzioni implementate
# nel modulo TES funzionino senza problemi

# per il notebook finale non vengono considerati ma è comunque buona norma verificarne
# il funzionamento prima di ogni commit

import unittest, tes
import numpy as np

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
    def test_coseno_rialzato_tempo(self):
        pass

    # test che prova la porta discreta in frequenza adoperando alcuni esempi
    # effettuati a mano
    def test_porta_frequenza(self):
        pass

    # test che prova il coseno rialzato in frequenza adoperando alcuni esempi
    # effettuati a mano
    def test_coseno_rialzato_frequenza(self):
        pass

    # test che prova la convoluzione scritta a mano rispetto a quella di libreria
    def test_conv(self):
        pass