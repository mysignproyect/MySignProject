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
        esperadas = [
            "Raíz", "Salud", "Hospitales", "Clínicas", "Centros de Salud",
            "Educación", "Colegios", "Universidades", "Institutos",
            "Gobierno", "Alcaldías", "Entidades Públicas",
            "Intérpretes", "Por Especialidad"
        ]
        for cat in esperadas:
            self.assertIn(cat, categorias)

    def test_cargar_servicios_en_arbol_sin_subcategoria(self):
        hospitales = self.arbol.buscar_servicios_categoria("Salud")
        gobierno = self.arbol.buscar_servicios_categoria("Gobierno")
        colegios = self.arbol.buscar_servicios_categoria("Educación")

        self.assertGreaterEqual(len(hospitales), 1)
        self.assertGreaterEqual(len(gobierno), 1)
        self.assertGreaterEqual(len(colegios), 1)

    def test_cargar_categoria__servicio_nuevo(self):
        raiz = self.arbol.raiz
        recreacion = raiz.add_subcategoria("Recreacion")
        for sub in ["Comunidades", "IG", "UsuarioComunidad"]:
            recreacion.add_subcategoria(sub)

        nuevo_servicio = {
            "id": 999,
            "nombre": "Evento Cultural",
            "categoria": "Recreacion",
            "subcategoria": "Comunidades",
            "descripcion": "Prueba temporal",
        }
        recreacion.subcategorias["Comunidades"].add_servicio(nuevo_servicio)

        resultado = self.arbol.buscar_servicios_categoria("Recreacion", "Comunidades")
        self.assertEqual(len(resultado), 1)


    def test_buscar_categoria_inexistente(self):
        resultado = self.arbol.buscar_servicios_categoria("Inexistente")
        self.assertEqual(resultado, [])


if __name__ == "__main__":
    unittest.main()
