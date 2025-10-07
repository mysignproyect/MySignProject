import unittest
from app.services.buscador import crear_buscador_desde_mock

class TestBuscadorServicios(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.buscador = crear_buscador_desde_mock()

    def test_buscar_servicio_por_id(self):
        servicio = self.buscador.buscar_servicio_por_id("s1")
        self.assertIsNotNone(servicio)
        self.assertEqual(servicio["nombre"], "Hospital San Vicente Fundación")

    def test_buscar_servicio_inexistente_por_id(self):
        servicio = self.buscador.buscar_servicio_por_id("z1")
        self.assertIsNone(servicio)

    def test_buscar_servicios_por_categoria(self):
        salud = self.buscador.buscar_servicios_por_categoria("Salud")
        self.assertEqual(len(salud), 3)
        self.assertTrue(all(s["categoria"] == "Salud" for s in salud))

    def test_buscar_servicios_inexistentes_por_categoria(self):
        prueba = self.buscador.buscar_servicios_por_categoria("Prueba")
        self.assertEqual(len(prueba), 0)

    def test_buscar_servicios_por_zona(self):
        norte = self.buscador.buscar_servicios_por_zona("Norte")
        self.assertTrue(any("Norte" == s["zona"] for s in norte))

    def test_buscar_servicios_por_zona_inexistente(self):
        zona = self.buscador.buscar_servicios_por_zona("NonexistentZone")
        self.assertFalse(zona)

    def test_filtrar_servicios_con_interprete(self):
        filtrados = self.buscador.filtrar_servicios(categoria="Salud", tiene_interprete=True)
        self.assertTrue(all(s["tiene_interprete_lsc"] for s in filtrados))

    def test_buscar_interprete_por_id(self):
        interprete = self.buscador.buscar_interprete_por_id("i2")
        self.assertIsNotNone(interprete)
        self.assertEqual(interprete["nombre"], "Carlos Restrepo Ramírez")

    def test_buscar_interpretes_por_especialidad(self):
        medicos = self.buscador.buscar_interpretes_por_especialidad("Médica")
        self.assertGreaterEqual(len(medicos), 1)
        self.assertTrue(all("Médica" in i["especialidades"] for i in medicos))


    def test_buscar_interpretes_por_especialidad_inexistente(self):
        interpretes = self.buscador.buscar_interpretes_por_especialidad("Inexistente")
        self.assertEqual(len(interpretes), 0)


if __name__ == "__main__":
    unittest.main()
