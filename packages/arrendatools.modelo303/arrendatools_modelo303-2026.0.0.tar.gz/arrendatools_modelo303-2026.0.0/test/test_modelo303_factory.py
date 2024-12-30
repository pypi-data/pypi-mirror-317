import unittest

from arrendatools.modelo303.datos import Modelo303Datos, Periodo
from arrendatools.modelo303.factory import Modelo303Factory
from arrendatools.modelo303.generadores.generador_ejercicio_2023 import (
    GeneradorEjercicio2023,
)
from arrendatools.modelo303.generadores.generador_ejercicio_2024 import (
    GeneradorEjercicio2024,
)
from arrendatools.modelo303.generadores.generador_ejercicio_2025 import (
    GeneradorEjercicio2025,
)


class Modelo303FactoryTestCase(unittest.TestCase):
    def setUp(self):
        self.datos = Modelo303Datos(
            periodo=Periodo.PRIMER_TRIMESTRE,
            base_imponible=1000,
            version="v1.0",
            nif_empresa_desarrollo="12345678X",
            nif_contribuyente="12345678E",
            nombre_fiscal_contribuyente="DE LOS PALOTES PERICO",
        )

    def test_get_modelo_303_2023(self):
        modelo = Modelo303Factory.obtener_generador_modelo303(2023)
        self.assertIsInstance(modelo, GeneradorEjercicio2023)

    def test_get_modelo_303_2024(self):
        modelo = Modelo303Factory.obtener_generador_modelo303(2024)
        self.assertIsInstance(modelo, GeneradorEjercicio2024)

    def test_get_modelo_303_2025(self):
        modelo = Modelo303Factory.obtener_generador_modelo303(2025)
        self.assertIsInstance(modelo, GeneradorEjercicio2025)

    def test_get_modelo_303_invalid_year(self):
        with self.assertRaises(ValueError):
            Modelo303Factory.obtener_generador_modelo303(2022)


if __name__ == "__main__":
    unittest.main()
