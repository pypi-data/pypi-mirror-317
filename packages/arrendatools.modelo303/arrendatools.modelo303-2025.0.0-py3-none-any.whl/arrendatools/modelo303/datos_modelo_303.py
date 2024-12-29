from enum import Enum

from pydantic import BaseModel, Field, model_validator

LONGITUD_NIF = 9
MAX_LONGITUD_VERSION = 4
MAX_LONGITUD_NOMBRE_FISCAL_CONTRIBUYENTE = 80
MAX_LONGITUD_IBAN = 24


class Periodo(str, Enum):
    PRIMER_TRIMESTRE = "1T"
    SEGUNDO_TRIMESTRE = "2T"
    TERCER_TRIMESTRE = "3T"
    CUARTO_TRIMESTRE = "4T"


class DatosModelo303(BaseModel):
    periodo: Periodo = Field(
        ..., description="Trimestre en formato 1T, 2T, 3T o 4T"
    )
    version: str = Field(
        ..., max_length=MAX_LONGITUD_VERSION, description="Versión"
    )
    nif_empresa_desarrollo: str = Field(
        ...,
        min_length=LONGITUD_NIF,
        max_length=LONGITUD_NIF,
        description="NIF de la empresa desarrolladora",
    )
    nombre_fiscal_contribuyente: str = Field(
        ...,
        max_length=MAX_LONGITUD_NOMBRE_FISCAL_CONTRIBUYENTE,
        description="Nombre fiscal del contribuyente",
    )
    nif_contribuyente: str = Field(
        ...,
        min_length=LONGITUD_NIF,
        max_length=LONGITUD_NIF,
        description="NIF del contribuyente",
    )
    iban: str = Field(
        "",
        min_length=MAX_LONGITUD_IBAN,
        max_length=MAX_LONGITUD_IBAN,
        description="IBAN de la cuenta bancaria",
    )
    base_imponible: float = Field(..., ge=0, description="Base imponible")
    gastos_bienes_servicios: float = Field(
        0, ge=0, description="Gastos en bienes y servicios"
    )
    iva_gastos_bienes_servicios: float = Field(
        0, ge=0, description="IVA soportado en bienes y servicios"
    )
    adquisiciones_bienes_inversion: float = Field(
        0, ge=0, description="Adquisiciones de bienes de inversión"
    )
    iva_adquisiciones_bienes_inversion: float = Field(
        0, ge=0, description="IVA soportado en bienes de inversión"
    )
    volumen_anual_operaciones: float | None = Field(
        None, ge=0, description="Volumen anual de operaciones"
    )

    @model_validator(mode="after")
    def check_volumen_anual_operaciones(self):
        if (
            self.periodo == Periodo.CUARTO_TRIMESTRE
            and self.volumen_anual_operaciones is None  # noqa W503
        ):
            raise ValueError(
                "El volumen anual de operaciones es obligatorio en el 4º trimestre (4T)"
            )
        return self
