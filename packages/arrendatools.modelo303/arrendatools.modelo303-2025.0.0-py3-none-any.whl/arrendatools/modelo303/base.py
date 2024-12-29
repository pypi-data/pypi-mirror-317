from abc import ABC, abstractmethod

from .datos_modelo_303 import DatosModelo303


class Modelo303Base(ABC):
    def __init__(self, ejercicio: int, datos: DatosModelo303):
        self.ejercicio = str(ejercicio)
        self.datos = datos

    @abstractmethod
    def generar(self) -> str:
        """
        Genera el string para la importación de datos en el modelo 303 de la Agencia Tributaria de España (PRE 303 - Servicio ayuda modelo 303).
        El string generado se puede guardar en un fichero y es compatible con el modelo 303 para la presentación trimestral del IVA.
        """
        pass
