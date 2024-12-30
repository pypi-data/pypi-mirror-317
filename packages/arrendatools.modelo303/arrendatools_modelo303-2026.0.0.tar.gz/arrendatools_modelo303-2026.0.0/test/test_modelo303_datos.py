import unittest

from pydantic import ValidationError

from arrendatools.modelo303.datos import Modelo303Datos, Periodo


class Modelo303DatosTestCase(unittest.TestCase):

    def setUp(self):
        # Datos base válidos
        self.datos_validos = {
            "periodo": Periodo.TERCER_TRIMESTRE,
            "version": "v1.0",
            "nif_empresa_desarrollo": "12345678X",
            "nombre_fiscal_contribuyente": "DE LOS PALOTES PERICO",
            "nif_contribuyente": "12345678E",
            "base_imponible": 2000.00,
        }

    def test_generar_modelo_4T_volumen_anual_None(self):
        self.datos_validos["periodo"] = Periodo.CUARTO_TRIMESTRE

        with self.assertRaisesRegex(
            ValueError,
            "El volumen anual de operaciones es obligatorio en el 4º trimestre*",
        ):
            Modelo303Datos(**self.datos_validos)

    def test_generar_modelo_nif_ed_largo(self):
        self.datos_validos["nif_empresa_desarrollo"] = (
            "12345678XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        )
        with self.assertRaises(ValidationError) as cm:
            Modelo303Datos(**self.datos_validos)
        self.assertIn("nif_empresa_desarrollo", str(cm.exception))

    def test_generar_modelo_nif_ed_corto(self):
        self.datos_validos["nif_empresa_desarrollo"] = "1234"
        with self.assertRaises(ValidationError) as cm:
            Modelo303Datos(**self.datos_validos)
        self.assertIn("nif_empresa_desarrollo", str(cm.exception))

    def test_generar_modelo_nif_contribuyente_largo(self):
        self.datos_validos["nif_contribuyente"] = (
            "12345678XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        )
        with self.assertRaises(ValidationError) as cm:
            Modelo303Datos(**self.datos_validos)
        self.assertIn("nif_contribuyente", str(cm.exception))

    def test_generar_modelo_nif_contribuyente_corto(self):
        self.datos_validos["nif_contribuyente"] = "1234"
        with self.assertRaises(ValidationError) as cm:
            Modelo303Datos(**self.datos_validos)
        self.assertIn("nif_contribuyente", str(cm.exception))

    def test_generar_modelo_version_largo(self):
        self.datos_validos["version"] = "1.234"
        with self.assertRaises(ValidationError) as cm:
            Modelo303Datos(**self.datos_validos)
        self.assertIn("version", str(cm.exception))

    def test_generar_modelo_nombre_largo(self):
        self.datos_validos["nombre_fiscal_contribuyente"] = (
            "DE LOS PALOTES PERICO PERO QUE SEA MAYOR DE LO PERMITIDO POR LA AGENCIA TRIBUTARIA"
        )
        with self.assertRaises(ValidationError) as cm:
            Modelo303Datos(**self.datos_validos)
        self.assertIn("nombre_fiscal_contribuyente", str(cm.exception))

    def test_generar_modelo_iban_largo(self):
        self.datos_validos["iban"] = "ES001234123412341234123412345678901"
        with self.assertRaises(ValidationError) as cm:
            Modelo303Datos(**self.datos_validos)
        self.assertIn("iban", str(cm.exception))

    def test_generar_modelo_base_imponible_negativa(self):
        self.datos_validos["base_imponible"] = -1000.00
        with self.assertRaises(ValidationError) as cm:
            Modelo303Datos(**self.datos_validos)
        self.assertIn("base_imponible", str(cm.exception))

    def test_generar_modelo_gastos_bienes_servicios_negativos(self):
        self.datos_validos["gastos_bienes_servicios"] = -500.00
        with self.assertRaises(ValidationError) as cm:
            Modelo303Datos(**self.datos_validos)
        self.assertIn("gastos_bienes_servicios", str(cm.exception))

    def test_generar_modelo_iva_gastos_bienes_servicios_negativos(self):
        self.datos_validos["iva_gastos_bienes_servicios"] = -100.00
        with self.assertRaises(ValidationError) as cm:
            Modelo303Datos(**self.datos_validos)
        self.assertIn("iva_gastos_bienes_servicios", str(cm.exception))

    def test_generar_modelo_adquisiciones_bienes_inversion_negativos(self):
        self.datos_validos["adquisiciones_bienes_inversion"] = -200.00
        with self.assertRaises(ValidationError) as cm:
            Modelo303Datos(**self.datos_validos)
        self.assertIn("adquisiciones_bienes_inversion", str(cm.exception))

    def test_generar_modelo_iva_adquisiciones_bienes_inversion_negativos(self):
        self.datos_validos["iva_adquisiciones_bienes_inversion"] = -50.00
        with self.assertRaises(ValidationError) as cm:
            Modelo303Datos(**self.datos_validos)
        self.assertIn("iva_adquisiciones_bienes_inversion", str(cm.exception))

    def test_generar_modelo_volumen_anual_operaciones_negativo(self):
        self.datos_validos["volumen_anual_operaciones"] = -10000.00
        with self.assertRaises(ValidationError) as cm:
            Modelo303Datos(**self.datos_validos)
        self.assertIn("volumen_anual_operaciones", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
