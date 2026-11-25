import random
import unittest
from algoritmos import lcs_dinamica, lcs_hirschberg, lcs_recursiva


def es_subsecuencia(candidata: str, texto: str) -> bool:
    iterador = iter(texto)
    return all(simbolo in iterador for simbolo in candidata)


class TestAlgoritmosLCS(unittest.TestCase):
    def test_casos_limite(self) -> None:
        casos = [
            ("", "", 0),
            ("", "ABCDE", 0),
            ("ABCDE", "", 0),
            ("A", "A", 1),
            ("A", "B", 0),
            ("ALGORITMO", "ALGORITMO", 9),
            ("AAAAA", "AA", 2),
            ("ABCDE", "FGHIJ", 0),
            ("ACCGGTCGAGT", "GTCGTTCGGAAT", 7),
        ]
        for cad_a, cad_b, long_esperada in casos:
            res_a = lcs_recursiva(cad_a, cad_b)
            res_b = lcs_hirschberg(cad_a, cad_b)
            res_c = lcs_dinamica(cad_a, cad_b)

            for res in (res_a, res_b, res_c):
                self.assertEqual(len(res), long_esperada)
                self.assertTrue(es_subsecuencia(res, cad_a))
                self.assertTrue(es_subsecuencia(res, cad_b))

            self.assertEqual(res_a, res_c)

    def test_aleatorios_pequenos_tres_versiones(self) -> None:
        rng = random.Random(7331)
        alfabeto = ["A", "B", "C", "D", "E"]
        for _ in range(150):
            m = rng.randint(1, 9)
            n = rng.randint(1, 9)
            cad_a = "".join(rng.choice(alfabeto) for _ in range(m))
            cad_b = "".join(rng.choice(alfabeto) for _ in range(n))

            res_a = lcs_recursiva(cad_a, cad_b)
            res_b = lcs_hirschberg(cad_a, cad_b)
            res_c = lcs_dinamica(cad_a, cad_b)

            self.assertEqual(res_a, res_c)
            self.assertEqual(len(res_b), len(res_c))
            self.assertTrue(es_subsecuencia(res_b, cad_a))
            self.assertTrue(es_subsecuencia(res_b, cad_b))

    def test_aleatorios_medianos_b_y_c(self) -> None:
        rng = random.Random(9001)
        alfabeto = ["A", "B", "C", "D", "E"]
        for _ in range(80):
            m = rng.randint(25, 110)
            n = rng.randint(25, 110)
            cad_a = "".join(rng.choice(alfabeto) for _ in range(m))
            cad_b = "".join(rng.choice(alfabeto) for _ in range(n))

            res_b = lcs_hirschberg(cad_a, cad_b)
            res_c = lcs_dinamica(cad_a, cad_b)

            self.assertEqual(len(res_b), len(res_c))
            self.assertTrue(es_subsecuencia(res_b, cad_a))
            self.assertTrue(es_subsecuencia(res_b, cad_b))
            self.assertTrue(es_subsecuencia(res_c, cad_a))
            self.assertTrue(es_subsecuencia(res_c, cad_b))


if __name__ == "__main__":
    unittest.main()
