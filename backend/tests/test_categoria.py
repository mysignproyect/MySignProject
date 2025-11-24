import unittest
import copy
from data.mock_data import SERVICIOS_MOCK
from app.services.categoria_tree import *


class TestNodoCategoria(unittest.TestCase):

    def test_creacion_nodo_categoria(self):
        """Valida que un nodo se cree correctamente con nombre, subcategorías vacías y lista de servicios vacía."""
        nodo = NodoCategoria("Salud")
        self.assertEqual(nodo.nombre, "Salud")
        self.assertEqual(nodo.subcategorias, {})
        self.assertEqual(nodo.servicios, [])

        sub = nodo.add_subcategoria("Hospitales")
        self.assertIn("Hospitales", nodo.subcategorias)
        self.assertIsInstance(sub, NodoCategoria)

    def test_agregar_servicios_en_nodo(self):
        """Valida que un servicio se agregue correctamente al nodo y se pueda acceder a él."""
        nodo = NodoCategoria("Educación")
        servicio = {"id": "s1", "nombre": "Colegio ABC"}
        nodo.add_servicio(servicio)
        self.assertEqual(len(nodo.servicios), 1)
        self.assertEqual(nodo.servicios[0]["id"], "s1")

    def test_es_raiz(self):
        """Verifica si un nodo se reconoce correctamente como raíz o hijo según corresponda."""
        raiz = NodoCategoria("Raíz")
        self.assertTrue(raiz.es_raiz)

        hijo = raiz.add_subcategoria("Hijo")
        self.assertFalse(hijo.es_raiz)

    def test_es_hoja(self):
        """Valida si un nodo se identifica correctamente como hoja o no hoja según tenga subcategorías."""
        nodo = NodoCategoria("Salud")
        self.assertTrue(nodo.es_hoja)

        nodo.add_subcategoria("Hospitales")
        self.assertFalse(nodo.es_hoja)

    def test_nivel_nodo(self):
        """Verifica que el nivel de los nodos se calcule correctamente según la profundidad en el árbol."""
        raiz = NodoCategoria("Raíz")
        hijo = raiz.add_subcategoria("Nivel1")
        nieto = hijo.add_subcategoria("Nivel2")

        self.assertEqual(raiz.nivel, 0)
        self.assertEqual(hijo.nivel, 1)
        self.assertEqual(nieto.nivel, 2)

    def test_nivel_y_hoja(self):
        """Valida niveles y si los nodos son hoja en un árbol precargado con datos mock."""
        arbol = inicializar_arbol_con_mock()
        raiz = arbol.raiz
        self.assertTrue(raiz.es_raiz)
        self.assertFalse(raiz.es_hoja)

        salud = raiz.subcategorias["Salud"]
        self.assertEqual(salud.nivel, 1)

        hospitales = salud.subcategorias["Hospitales"]
        self.assertTrue(hospitales.es_hoja)
        self.assertEqual(hospitales.nivel, 2)


class TestArbolCategorias(unittest.TestCase):
    def setUp(self):
        self.servicios_backup = copy.deepcopy(SERVICIOS_MOCK)
        self.arbol = inicializar_arbol_con_mock()

    def tearDown(self):
        del self.arbol
        SERVICIOS_MOCK.clear()
        SERVICIOS_MOCK.extend(copy.deepcopy(self.servicios_backup))

    def test_validar_existencia_de_las_categorias(self):
        """Verifica que las categorías principales estén presentes en el árbol."""
        categorias = self.arbol.obtener_todas_categorias()
        esperadas = ["Salud", "Educación", "Gobierno"]
        self.assertCountEqual(categorias, esperadas)

    def test_obtener_subcategorias(self):
        """Valida que se puedan obtener correctamente las subcategorías de cada categoría principal."""
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
        """Valida que obtener subcategorías de una categoría inexistente retorne lista vacía."""
        sub_inexistente = self.arbol.obtener_subcategorias("Inexistente")
        self.assertEqual(sub_inexistente, [])

    def test_buscar_subcategoria_existente(self):
        """Verifica que la búsqueda de servicios en una subcategoría existente retorne una lista con servicios válidos."""
        resultado = self.arbol.buscar_servicios_categoria("Salud", "Hospitales")
        self.assertIsInstance(resultado, list)
        for s in resultado:
            self.assertIn("categoria", s)
            self.assertIn("nombre", s)

    def test_cargar_servicios_en_arbol_sin_subcategoria(self):
        """Valida que los servicios se carguen correctamente en categorías existentes sin subcategoría específica."""
        hospitales = self.arbol.buscar_servicios_categoria("Salud")
        gobierno = self.arbol.buscar_servicios_categoria("Gobierno")
        colegios = self.arbol.buscar_servicios_categoria("Educación")

        self.assertGreaterEqual(len(hospitales), 1)
        self.assertGreaterEqual(len(gobierno), 1)
        self.assertGreaterEqual(len(colegios), 1)

    def test_buscar_categoria_inexistente(self):
        """Verifica que la búsqueda en una categoría inexistente retorne lista vacía."""
        resultado = self.arbol.buscar_servicios_categoria("Inexistente")
        self.assertEqual(resultado, [])

    def test_buscar_categoria_sin_subcategoria(self):
        """Valida que la búsqueda en una categoría existente sin subcategoría retorne lista de servicios."""
        resultado = self.arbol.buscar_servicios_categoria("Educación")
        self.assertIsInstance(resultado, list)

    def test_cargar_servicios_en_subcategoria_existente(self):
        """Verifica que un servicio se agregue correctamente en una subcategoría existente."""
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
        """Valida que un servicio con subcategoría no existente se agregue a la categoría principal."""
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

    def test_buscar_subcategoria_vacia(self):
        """Verifica que la búsqueda en una subcategoría vacía retorne lista vacía."""
        vacios = self.arbol.buscar_servicios_categoria("Educación", "Institutos")
        self.assertEqual(vacios, [])

    def test_cargar_servicios_crea_categoria_nueva(self):
        """Valida que al cargar un servicio con categoría inexistente, el árbol cree la categoría automáticamente."""
        servicio = {
            "id": "s3",
            "nombre": "Museo Nacional",
            "categoria": "Cultura",
            "subcategoria": "Museos",
            "descripcion": "Debe crear la categoría nueva automáticamente",
        }

        self.arbol.cargar_servicios([servicio])

        categorias = self.arbol.obtener_todas_categorias()
        self.assertIn(
            "Cultura", categorias, "La categoría nueva no fue creada automáticamente."
        )

        resultado = self.arbol.buscar_servicios_categoria("Cultura")
        self.assertTrue(any(s["id"] == "s3" for s in resultado))


if __name__ == "__main__":
    unittest.main()
