import unittest
import pytest
from app.utils.pagination import *


class TestPaginarResultados(unittest.TestCase):
    def setUp(self):
        self.items = list(range(1, 11))

    def test_paginacion_basica(self):
        """
        Verifica la paginación de un conjunto de datos en una página intermedia.
        Comprueba los datos de la página y la metadata de navegación.
        """
        resultado = paginar_resultados(self.items, page=2, limit=3)
        self.assertEqual(resultado["data"], [4, 5, 6])
        meta = resultado["metadata"]
        self.assertEqual(meta["current_page"], 2)
        self.assertEqual(meta["page_size"], 3)
        self.assertTrue(meta["has_next"])
        self.assertTrue(meta["has_previous"])

    def test_pagina_final_incompleta(self):
        """
        Asegura que la última página maneje correctamente un número de ítems menor al límite.
        Verifica el tamaño de página real y que 'has_next' sea False.
        """
        resultado = paginar_resultados(self.items, page=4, limit=3)
        self.assertEqual(resultado["data"], [10])
        meta = resultado["metadata"]
        self.assertEqual(meta["page_size"], 1)
        self.assertFalse(meta["has_next"])
        self.assertTrue(meta["has_previous"])

    def test_pagina_fuera_de_rango(self):
        """
        Comprueba que si se solicita una página superior al total, se devuelva la última página.
        """
        resultado = paginar_resultados(self.items, page=10, limit=4)
        self.assertEqual(resultado["metadata"]["current_page"], 3)
        self.assertEqual(resultado["data"], [9, 10])

    def test_lista_vacia(self):
        """
        Valida el comportamiento de la paginación cuando se le pasa una lista de ítems vacía.
        """
        resultado = paginar_resultados([], page=1, limit=5)
        self.assertEqual(resultado["data"], [])
        self.assertEqual(resultado["metadata"]["total_pages"], 1)
        self.assertEqual(resultado["metadata"]["current_page"], 1)
        self.assertFalse(resultado["metadata"]["has_next"])

    def test_error_pagina_invalida(self):
        """
        Verifica que se lance una excepción de valor si el número de página es menor o igual a cero.
        """
        with self.assertRaises(ValueError):
            paginar_resultados(self.items, page=0, limit=5)

    def test_error_limite_invalido_menor(self):
        """
        Asegura que se lance una excepción si el límite de ítems por página es menor o igual a cero.
        """
        with self.assertRaises(ValueError):
            paginar_resultados(self.items, page=1, limit=0)

    def test_error_limite_invalido_mayor(self):
        """
        Comprueba que se lance una excepción si el límite de ítems por página excede un máximo predefinido (50).
        """
        with self.assertRaises(ValueError):
            paginar_resultados(self.items, page=1, limit=100)

    def test_paginacion_unica_pagina(self):
        """
        Prueba la paginación cuando el límite es mayor que el total de ítems, resultando en una sola página.
        """
        resultado = paginar_resultados(self.items, page=1, limit=20)
        self.assertEqual(resultado["data"], self.items)
        meta = resultado["metadata"]
        self.assertEqual(meta["total_pages"], 1)
        self.assertFalse(meta["has_next"])
        self.assertFalse(meta["has_previous"])

    def test_metadata_to_dict(self):
        """
        Verifica la correcta conversión del objeto MetadataPaginacion a un diccionario para la respuesta.
        """
        meta = MetadataPaginacion(
            total_items=10,
            total_pages=2,
            current_page=1,
            page_size=5,
            has_next=True,
            has_previous=False
        )
        d = meta.to_dict()
        self.assertEqual(d["total_items"], 10)
        self.assertEqual(d["total_pages"], 2)
        self.assertEqual(d["current_page"], 1)
        self.assertEqual(d["page_size"], 5)
        self.assertTrue(d["has_next"])
        self.assertFalse(d["has_previous"])

    def test_metadata_generada_por_paginar(self):
        """
        Confirma que la metadata generada por la función 'paginar_resultados' es precisa.
        """
        items = list(range(1, 21))
        resultado = paginar_resultados(items, page=2, limit=10)
        meta = resultado["metadata"]

        assert meta["total_items"] == 20
        assert meta["total_pages"] == 2
        assert meta["current_page"] == 2
        assert meta["page_size"] == 10
        assert meta["has_previous"] is True
        assert meta["has_next"] is False


    def test_pagina_mayor_con_lista_vacia(self):
        """
        Prueba que, incluso si se pide una página alta, una lista vacía siempre devuelve la página 1 sin datos.
        """
        resultado = paginar_resultados([], page=5, limit=10)
        self.assertEqual(resultado["metadata"]["current_page"], 1)
        self.assertEqual(resultado["data"], [])

    def test_limite_minimo_valido(self):
        """
        Valida el caso extremo de paginación con un límite de 1 ítem por página.
        """
        resultado = paginar_resultados(self.items, page=1, limit=1)
        self.assertEqual(resultado["data"], [1])
        self.assertTrue(resultado["metadata"]["has_next"])
        self.assertFalse(resultado["metadata"]["has_previous"])

    def test_limite_maximo_valido(self):
        """
        Verifica el caso extremo de paginación con el límite máximo permitido (50).
        """
        resultado = paginar_resultados(self.items, page=1, limit=50)
        self.assertEqual(resultado["data"], self.items)
        self.assertEqual(resultado["metadata"]["total_pages"], 1)

    def test_pagina_uno_basica(self):
        """
        Comprueba la primera página de un conjunto de datos paginado.
        """
        resultado = paginar_resultados(self.items, page=1, limit=3)
        self.assertEqual(resultado["data"], [1, 2, 3])
        self.assertTrue(resultado["metadata"]["has_next"])
        self.assertFalse(resultado["metadata"]["has_previous"])

    def test_multiplo_exactos(self):
        """
        Asegura la correcta paginación cuando el total de ítems es múltiplo exacto del límite.
        """
        items = list(range(1, 11))
        resultado = paginar_resultados(items, page=2, limit=5)
        self.assertEqual(resultado["data"], [6, 7, 8, 9, 10])
        self.assertFalse(resultado["metadata"]["has_next"])
        self.assertTrue(resultado["metadata"]["has_previous"])

    def test_limite_grande_con_lista_vacia(self):
        """
        Verifica la metadata para una lista vacía con un límite de página grande.
        """
        resultado = paginar_resultados([], page=1, limit=50)
        meta = resultado["metadata"]
        self.assertEqual(meta["total_items"], 0)
        self.assertEqual(meta["total_pages"], 1)
        self.assertEqual(meta["page_size"], 0)
        self.assertFalse(meta["has_next"])
        self.assertFalse(meta["has_previous"])

    def test_paginar_directo(self):
        """
        Prueba la función estática 'Paginador.paginar' directamente.
        """
        items = list(range(1, 6))
        resultado = Paginador.paginar(items, page=1, limit=2)
        assert resultado["data"] == [1, 2]
        assert resultado["metadata"]["current_page"] == 1

    def test_paginar_page_mayor_directo(self):
        """
        Comprueba el ajuste de página cuando se solicita una página fuera de rango usando el método directo.
        """
        items = list(range(1, 6)) 
        resultado = Paginador.paginar(items, page=10, limit=2)
        assert resultado["metadata"]["current_page"] == 3

    def test_paginacion_limit_1_varias_paginas(self):
        """
        Valida la paginación de un dataset en la última página con un límite de 1 ítem.
        """
        items = [1, 2, 3]
        resultado = paginar_resultados(items, page=3, limit=1)
        assert resultado["data"] == [3]

    def test_paginacion_con_objetos(self):
        """
        Asegura que la paginación funcione correctamente con listas de objetos (no primitivos).
        """
        class X: pass
        objs = [X(), X(), X()]
        resultado = paginar_resultados(objs, page=1, limit=2)
        assert len(resultado["data"]) == 2

    def test_paginacion_con_strings(self):
        """
        Verifica el funcionamiento de la paginación con una lista de cadenas de texto.
        """
        items = ["a", "b", "c", "d"]
        res = paginar_resultados(items, page=2, limit=2)
        assert res["data"] == ["c", "d"]

    def test_limite_minimo_directo(self):
        """
        Prueba el límite mínimo de 1 ítem usando la función estática 'Paginador.paginar'.
        """
        items = [1, 2, 3]
        res = Paginador.paginar(items, page=1, limit=1)
        assert res["data"] == [1]

    def test_limite_maximo_directo(self):
        """
        Prueba el límite máximo de 50 ítems usando la función estática 'Paginador.paginar'.
        """
        items = [1, 2, 3]
        res = Paginador.paginar(items, page=1, limit=50)
        assert res["data"] == items

    def test_error_pagina_invalida_directo(self):
        """
        Asegura que el método directo lance 'ValueError' si la página solicitada es inválida (menor o igual a cero).
        """
        with pytest.raises(ValueError):
            Paginador.paginar([1, 2, 3], page=0, limit=5)

if __name__ == "__main__":
    unittest.main()