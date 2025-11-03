import unittest
from app.utils.pagination import *


class TestPaginarResultados(unittest.TestCase):
    def setUp(self):
        self.items = list(range(1, 11))

    
    def test_paginacion_basica(self):
        resultado = paginar_resultados(self.items, page=2, limit=3)
        self.assertEqual(resultado["data"], [4, 5, 6])
        meta = resultado["metadata"]
        self.assertEqual(meta["current_page"], 2)
        self.assertEqual(meta["page_size"], 3)
        self.assertTrue(meta["has_next"])
        self.assertTrue(meta["has_previous"])

    def test_pagina_final_incompleta(self):
        resultado = paginar_resultados(self.items, page=4, limit=3)
        self.assertEqual(resultado["data"], [10])
        meta = resultado["metadata"]
        self.assertEqual(meta["page_size"], 1)
        self.assertFalse(meta["has_next"])
        self.assertTrue(meta["has_previous"])

    def test_pagina_fuera_de_rango(self):
        resultado = paginar_resultados(self.items, page=10, limit=4)
        self.assertEqual(resultado["metadata"]["current_page"], 3)
        self.assertEqual(resultado["data"], [9, 10])

    def test_lista_vacia(self):
        resultado = paginar_resultados([], page=1, limit=5)
        self.assertEqual(resultado["data"], [])
        self.assertEqual(resultado["metadata"]["total_pages"], 1)
        self.assertEqual(resultado["metadata"]["current_page"], 1)
        self.assertFalse(resultado["metadata"]["has_next"])


    def test_error_pagina_invalida(self):
        with self.assertRaises(ValueError):
            paginar_resultados(self.items, page=0, limit=5)

    def test_error_limite_invalido_menor(self):
        with self.assertRaises(ValueError):
            paginar_resultados(self.items, page=1, limit=0)

    def test_error_limite_invalido_mayor(self):
        with self.assertRaises(ValueError):
            paginar_resultados(self.items, page=1, limit=100)


    def test_paginacion_unica_pagina(self):
        resultado = paginar_resultados(self.items, page=1, limit=20)
        self.assertEqual(resultado["data"], self.items)
        meta = resultado["metadata"]
        self.assertEqual(meta["total_pages"], 1)
        self.assertFalse(meta["has_next"])
        self.assertFalse(meta["has_previous"])


if __name__ == "__main__":
    unittest.main()
