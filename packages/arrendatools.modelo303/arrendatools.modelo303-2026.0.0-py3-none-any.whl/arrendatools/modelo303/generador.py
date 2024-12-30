from abc import ABC, abstractmethod

from arrendatools.modelo303.datos import Modelo303Datos


class Modelo303Generador(ABC):
    def __init__(self, ejercicio: int):
        self.ejercicio = str(ejercicio)

    @abstractmethod
    def generar(self, datos: Modelo303Datos) -> str:
        """
        Genera el string para la importación de datos en el modelo 303 de la Agencia Tributaria de España (PRE 303 - Servicio ayuda modelo 303).
        El string generado se puede guardar en un fichero y es compatible con el modelo 303 para la presentación trimestral del IVA.
        """
        raise NotImplementedError
