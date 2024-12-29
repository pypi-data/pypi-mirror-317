from .datos_modelo_303 import DatosModelo303
from .ejercicio_2023 import Modelo303Ejercicio2023
from .ejercicio_2024 import Modelo303Ejercicio2024
from .ejercicio_2025 import Modelo303Ejercicio2025


def get_modelo_303(ejercicio: int, datos: DatosModelo303):
    if ejercicio == 2023:
        return Modelo303Ejercicio2023(ejercicio, datos)
    elif ejercicio == 2024:
        return Modelo303Ejercicio2024(ejercicio, datos)
    elif ejercicio == 2025:
        return Modelo303Ejercicio2025(ejercicio, datos)
    else:
        raise ValueError(
            f"No hay implementación del modelo 303 para el ejercicio {ejercicio}."
        )
