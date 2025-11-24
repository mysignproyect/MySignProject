import unittest

from app.services.buscador import crear_buscador_desde_mock


class TestBuscadorServicios(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.buscador = crear_buscador_desde_mock()

    def test_buscar_servicio_por_id(self):
        """
        Verifica la recuperación exitosa de un servicio específico utilizando un ID válido.
        """
        servicio = self.buscador.buscar_servicio_por_id("s1")
        self.assertIsNotNone(servicio)
        self.assertEqual(servicio["nombre"], "Hospital San Vicente Fundación")

    def test_buscar_servicio_inexistente_por_id(self):
        """
        Prueba que la búsqueda de un servicio con un ID no existente devuelva 'None'.
        """
        servicio = self.buscador.buscar_servicio_por_id("z1")
        self.assertIsNone(servicio)

    def test_buscar_servicios_por_categoria(self):
        """
        Confirma que se pueden listar todos los servicios que pertenecen a una categoría dada (e.g., 'Salud').
        """
        salud = self.buscador.buscar_servicios_por_categoria("Salud")
        self.assertEqual(len(salud), 6)
        self.assertTrue(all(s["categoria"] == "Salud" for s in salud))

    def test_buscar_servicios_inexistentes_por_categoria(self):
        """
        Asegura que la búsqueda por una categoría no existente retorne una lista vacía.
        """
        prueba = self.buscador.buscar_servicios_por_categoria("Prueba")
        self.assertEqual(len(prueba), 0)

    def test_buscar_servicios_por_zona(self):
        """
        Valida que se encuentren servicios específicos al filtrar por una zona geográfica (e.g., 'Norte').
        """
        norte = self.buscador.buscar_servicios_por_zona("Norte")
        self.assertTrue(any("Norte" == s["zona"] for s in norte))

    def test_buscar_servicios_por_zona_inexistente(self):
        """
        Comprueba que la búsqueda por una zona sin servicios asociados no arroje resultados.
        """
        zona = self.buscador.buscar_servicios_por_zona("NonexistentZone")
        self.assertFalse(zona)

    def test_filtrar_servicios_con_interprete(self):
        """
        Evalúa el filtrado de servicios para incluir solo aquellos que tienen un intérprete LSC asignado.
        """
        filtrados = self.buscador.filtrar_servicios(
            categoria="Salud", tiene_interprete=True
        )
        self.assertTrue(all(s["tiene_interprete_lsc"] for s in filtrados))

    def test_buscar_interprete_por_id(self):
        """
        Verifica la recuperación de los detalles de un intérprete utilizando su ID único.
        """
        interprete = self.buscador.buscar_interprete_por_id("i2")
        self.assertIsNotNone(interprete)
        self.assertEqual(interprete["nombre"], "Carlos Restrepo Ramírez")

    def test_buscar_interpretes_por_especialidad(self):
        """
        Confirma la búsqueda de intérpretes basándose en una especialidad específica (e.g., 'Médica').
        """
        medicos = self.buscador.buscar_interpretes_por_especialidad("Médica")
        self.assertGreaterEqual(len(medicos), 1)
        self.assertTrue(all("Médica" in i["especialidades"] for i in medicos))

    def test_buscar_interpretes_por_especialidad_inexistente(self):
        """
        Asegura que la búsqueda por una especialidad no registrada devuelva una lista vacía.
        """
        interpretes = self.buscador.buscar_interpretes_por_especialidad("Inexistente")
        self.assertEqual(len(interpretes), 0)

    def test_filtrar_servicios_por_subcategoria(self):
        """
        Prueba el filtrado de servicios por una subcategoría específica dentro de una categoría mayor.
        """
        resultado = self.buscador.filtrar_servicios(
            categoria="Salud", subcategoria="Hospital General"
        )
        self.assertGreater(
            len(resultado),
            0,
            "No se encontraron servicios en la subcategoría 'Hospital General'.",
        )
        self.assertTrue(
            all(s["subcategoria"] == "Hospital General" for s in resultado),
            "Se encontraron servicios que no pertenecen a la subcategoría 'Hospital General'.",
        )

    def test_buscar_servicios_por_texto_en_nombre(self):
        """
        Valida que se encuentren servicios con texto coincidente en el campo 'nombre'.
        """
        resultados = self.buscador.buscar_servicios_por_texto("hospital")
        self.assertTrue(len(resultados) > 0)

    def test_buscar_servicios_por_texto_en_direccion(self):
        """
        Comprueba la búsqueda de servicios usando texto contenido en su dirección física.
        """
        resultados = self.buscador.buscar_servicios_por_texto("calle")
        self.assertIsInstance(resultados, list)

    def test_buscar_servicios_por_texto_en_caracteristicas(self):
        """
        Verifica la capacidad de búsqueda por texto presente en las características del servicio (e.g., 'rampa').
        """
        resultados = self.buscador.buscar_servicios_por_texto("rampa")
        self.assertIsInstance(resultados, list)

    def test_filtrar_servicios_sin_coincidencias(self):
        """
        Asegura que la aplicación de filtros sin resultados devuelva una lista de servicios vacía.
        """
        resultado = self.buscador.filtrar_servicios(
            categoria="Salud", zona="Fantasma"
        )
        self.assertEqual(resultado, [])

    def test_filtrar_servicios_sin_interprete(self):
        """
        Evalúa el filtrado para obtener solo los servicios que NO tienen un intérprete LSC asignado.
        """
        resultado = self.buscador.filtrar_servicios(tiene_interprete=False)
        self.assertTrue(all(not s["tiene_interprete_lsc"] for s in resultado))

    def test_buscar_interpretes_por_zona(self):
        """
        Prueba la funcionalidad de buscar intérpretes cuya zona de operación coincida con el filtro.
        """
        interpretes = self.buscador.buscar_interpretes_por_zona("Norte")
        self.assertIsInstance(interpretes, list)

    def test_buscar_interpretes_por_zona_inexistente(self):
        """
        Comprueba que no se encuentren intérpretes en una zona geográfica no cubierta.
        """
        interpretes = self.buscador.buscar_interpretes_por_zona("Atlantida")
        self.assertEqual(interpretes, [])

    def test_filtrar_interpretes_por_zona(self):
        """
        Confirma que el filtro de zona se aplica correctamente a la lista de intérpretes.
        """
        interpretes = self.buscador.filtrar_interpretes(zona="Sur")
        self.assertIsInstance(interpretes, list)

    def test_filtrar_interpretes_por_disponibilidad(self):
        """
        Verifica el filtrado de intérpretes en base a su estado de disponibilidad (e.g., 'inmediata').
        """
        interpretes = self.buscador.filtrar_interpretes(disponibilidad="inmediata")
        self.assertIsInstance(interpretes, list)

    def test_filtrar_interpretes_por_disponibilidad_inexistente(self):
        """
        Asegura que el manejo de un criterio de disponibilidad no válido no cause errores y devuelva una lista.
        """
        interpretes = self.buscador.filtrar_interpretes(disponibilidad="xxxxxx")
        self.assertIsInstance(interpretes, list)

    def test_filtrar_interpretes_sin_coincidencias(self):
        """
        Prueba que la combinación de filtros restrictivos en intérpretes (e.g., especialidad + zona) devuelva una lista vacía.
        """
        interpretes = self.buscador.filtrar_interpretes(
            especialidad="Médica",
            zona="ZonaInexistente"
        )
        self.assertEqual(interpretes, [])

    def test_obtener_todas_categorias(self):
        """
        Verifica que se recupera correctamente la lista completa de todas las categorías de servicios disponibles.
        """
        categorias = self.buscador.obtener_todas_categorias()
        self.assertIsInstance(categorias, list)
        self.assertGreater(len(categorias), 0)


if __name__ == "__main__":
    unittest.main()