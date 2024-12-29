import unittest

from pydantic import ValidationError

from arrendatools.modelo303.datos_modelo_303 import DatosModelo303, Periodo


class Modelo303Ejercicio2023TestCase(unittest.TestCase):
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
            DatosModelo303(**self.datos_validos)

    def test_generar_modelo_nif_ed_largo(self):
        self.datos_validos["nif_empresa_desarrollo"] = (
            "12345678XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        )
        with self.assertRaises(ValidationError) as cm:
            DatosModelo303(**self.datos_validos)
        self.assertIn("nif_empresa_desarrollo", str(cm.exception))

    def test_generar_modelo_nif_ed_corto(self):
        self.datos_validos["nif_empresa_desarrollo"] = "1234"
        with self.assertRaises(ValidationError) as cm:
            DatosModelo303(**self.datos_validos)
        self.assertIn("nif_empresa_desarrollo", str(cm.exception))

    def test_generar_modelo_nif_contribuyente_largo(self):
        self.datos_validos["nif_contribuyente"] = (
            "12345678XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        )
        with self.assertRaises(ValidationError) as cm:
            DatosModelo303(**self.datos_validos)
        self.assertIn("nif_contribuyente", str(cm.exception))

    def test_generar_modelo_nif_contribuyente_corto(self):
        self.datos_validos["nif_contribuyente"] = "1234"
        with self.assertRaises(ValidationError) as cm:
            DatosModelo303(**self.datos_validos)
        self.assertIn("nif_contribuyente", str(cm.exception))

    def test_generar_modelo_version_largo(self):
        self.datos_validos["version"] = "1.234"
        with self.assertRaises(ValidationError) as cm:
            DatosModelo303(**self.datos_validos)
        self.assertIn("version", str(cm.exception))

    def test_generar_modelo_nombre_largo(self):
        self.datos_validos["nombre_fiscal_contribuyente"] = (
            "DE LOS PALOTES PERICO PERO QUE SEA MAYOR DE LO PERMITIDO POR LA AGENCIA TRIBUTARIA"
        )
        with self.assertRaises(ValidationError) as cm:
            DatosModelo303(**self.datos_validos)
        self.assertIn("nombre_fiscal_contribuyente", str(cm.exception))

    def test_generar_modelo_iban_largo(self):
        self.datos_validos["iban"] = "ES001234123412341234123412345678901"
        with self.assertRaises(ValidationError) as cm:
            DatosModelo303(**self.datos_validos)
        self.assertIn("iban", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
