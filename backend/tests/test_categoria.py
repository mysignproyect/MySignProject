
import unittest
import copy
from data.mock_data import SERVICIOS_MOCK
from app.services.categoria_tree import *


class TestNodoCategoria(unittest.TestCase):
    def test_creacion_nodo_categoria(self):
        nodo = NodoCategoria("Salud")
        self.assertEqual(nodo.nombre, "Salud")
        self.assertEqual(nodo.subcategorias, {})
        self.assertEqual(nodo.servicios, [])

        sub = nodo.add_subcategoria("Hospitales")
        self.assertIn("Hospitales", nodo.subcategorias)
        self.assertIsInstance(sub, NodoCategoria)

    def test_agregar_servicios_en_nodo(self):
        nodo = NodoCategoria("Educación")
        servicio = {"id": "s1", "nombre": "Colegio ABC"}
        nodo.add_servicio(servicio)
        self.assertEqual(len(nodo.servicios), 1)
        self.assertEqual(nodo.servicios[0]["id"], "s1")


class TestArbolCategorias(unittest.TestCase):
    def setUp(self):
        self.servicios_backup = copy.deepcopy(SERVICIOS_MOCK)
        self.arbol = inicializar_arbol_con_mock()

    def tearDown(self):
        del self.arbol
        SERVICIOS_MOCK.clear()
        SERVICIOS_MOCK.extend(copy.deepcopy(self.servicios_backup))

    def test_validar_existencia_de_las_categorias(self):
        categorias = self.arbol.obtener_todas_categorias()
        esperadas = ["Salud", "Educación", "Gobierno", "Comercio", "Cultura"]
        self.assertCountEqual(categorias, esperadas)

    def test_obtener_subcategorias(self):
        sub_salud = self.arbol.obtener_subcategorias("Salud")
        esperadas_salud = ["Hospitales", "Clínicas", "Centros de Salud"]
        self.assertCountEqual(sub_salud, esperadas_salud)

        sub_educacion = self.arbol.obtener_subcategorias("Educación")
        esperadas_edu = ["Colegios", "Universidades", "Institutos"]
        self.assertCountEqual(sub_educacion, esperadas_edu)

        sub_gobierno = self.arbol.obtener_subcategorias("Gobierno")
        esperadas_gob = ["Alcaldías", "Entidades Públicas"]
        self.assertCountEqual(sub_gobierno, esperadas_gob)

        sub_comercio = self.arbol.obtener_subcategorias("Comercio")
        self.assertIsInstance(sub_comercio, list)

        sub_cultura = self.arbol.obtener_subcategorias("Cultura")
        self.assertIsInstance(sub_cultura, list)


    def test_obtener_subcategorias_inexistente(self):
        sub_inexistente = self.arbol.obtener_subcategorias("Inexistente")
        self.assertEqual(sub_inexistente, [])

    def test_buscar_subcategoria_existente(self):
        resultado = self.arbol.buscar_servicios_categoria("Salud", "Hospitales")
        self.assertIsInstance(resultado, list)
        for s in resultado:
            self.assertIn("categoria", s)
            self.assertIn("nombre", s)

    def test_cargar_servicios_en_arbol_sin_subcategoria(self):
        hospitales = self.arbol.buscar_servicios_categoria("Salud")
        gobierno = self.arbol.buscar_servicios_categoria("Gobierno")
        colegios = self.arbol.buscar_servicios_categoria("Educación")

        self.assertGreaterEqual(len(hospitales), 1)
        self.assertGreaterEqual(len(gobierno), 1)
        self.assertGreaterEqual(len(colegios), 1)

    def test_buscar_categoria_inexistente(self):
        resultado = self.arbol.buscar_servicios_categoria("Inexistente")
        self.assertEqual(resultado, [])
    
    def test_buscar_categoria_sin_subcategoria(self):
        resultado = self.arbol.buscar_servicios_categoria("Educación")
        self.assertIsInstance(resultado, list)
    
    def test_cargar_servicios_en_subcategoria_existente(self):
        servicio = {
            "id": "s1",
            "nombre": "Clínica Ejemplo",
            "categoria": "Salud",
            "subcategoria": "Clínicas",
            "descripcion": "Debe ir dentro de la subcategoría existente",
        }

        self.arbol.cargar_servicios([servicio])

        resultado = self.arbol.buscar_servicios_categoria("Salud", "Clínicas")
        self.assertTrue(any(s["id"] == "s1" for s in resultado))

    def test_cargar_servicios_en_categoria_existente_sin_subcategoria(self):
        servicio = {
            "id": "s2",
            "nombre": "Hospital General",
            "categoria": "Salud",
            "subcategoria": "NoExiste",
            "descripcion": "Debe agregarse directamente a la categoría principal",
        }

        self.arbol.cargar_servicios([servicio])

        resultado = self.arbol.buscar_servicios_categoria("Salud")
        self.assertTrue(any(s["id"] == "s2" for s in resultado))

    def test_cargar_servicios_crea_categoria_nueva(self):
        servicio = {
            "id": "s3",
            "nombre": "Museo Nacional",
            "categoria": "Cultura",
            "subcategoria": "Museos",
            "descripcion": "Debe crear la categoría nueva automáticamente",
        }

        self.arbol.cargar_servicios([servicio])

        categorias = self.arbol.obtener_todas_categorias()
        self.assertIn("Cultura", categorias, "La categoría nueva no fue creada automáticamente.")

        resultado = self.arbol.buscar_servicios_categoria("Cultura")
        self.assertTrue(any(s["id"] == "s3" for s in resultado))



if __name__ == "__main__":
    unittest.main()