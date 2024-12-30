import importlib
from pathlib import Path
from typing import Any

from arrendatools.modelo303.generador import Modelo303Generador


class Modelo303Factory:
    _GENERADORES_PATH = Path(__file__).parent / "generadores"
    _GENERADOR_PREFIX = "generador_ejercicio_"

    _EJERCICIO_MIN = 2023
    _EJERCICIO_MAX = 2050

    # Generar el conjunto dinámico de módulos seguros
    _SAFE_MODULES = {
        f"arrendatools.modelo303.generadores.generador_ejercicio_{ejercicio}"
        for ejercicio in range(_EJERCICIO_MIN, _EJERCICIO_MAX + 1)
    }

    @staticmethod
    def _load_class(module_class: str, safe_modules: set[str]) -> Any:
        """
        Carga dinámicamente una clase de un módulo si el módulo está en la lista blanca.

        Args:
            module_class (str): Nombre completo de la clase en formato 'modulo.clase'.
            safe_modules (set[str]): Conjunto de módulos permitidos.

        Returns:
            Any: Clase importada.

        Raises:
            ImportError: Si el módulo no está en la lista blanca o no se puede cargar la clase.
        """
        try:
            module_name, class_name = module_class.rsplit(".", 1)
        except ValueError:
            raise ImportError(
                f"Formato inválido para 'module_class': {module_class}"
            )

        if not class_name.isidentifier():
            raise ValueError(
                f"El nombre de la clase '{class_name}' no es válido"
            )

        if module_name not in safe_modules:
            raise ImportError(
                f"El módulo '{module_name}' no está en la lista blanca"
            )

        try:
            module = importlib.import_module(module_name)
            return getattr(module, class_name)
        except (ImportError, AttributeError) as e:
            raise ImportError(
                f"No se pudo cargar la clase '{class_name}' del módulo '{module_name}': {e}"
            )

    @staticmethod
    def obtener_generador_modelo303(ejercicio: int) -> Modelo303Generador:
        """Obtiene el generador del modelo 303 para el ejercicio especificado."""
        module_class = f"arrendatools.modelo303.generadores.generador_ejercicio_{ejercicio}.GeneradorEjercicio{ejercicio}"

        # Construir la ruta esperada del archivo
        ruta_modulo = (
            Modelo303Factory._GENERADORES_PATH
            / f"{Modelo303Factory._GENERADOR_PREFIX}{ejercicio}.py"
        )

        # Comprobación de seguridad de que exista el fichero del módulo
        if not ruta_modulo.exists():
            raise ValueError(
                f"No existe un generador para el ejercicio {ejercicio}"
            )

        try:
            generador_clase = Modelo303Factory._load_class(
                module_class, Modelo303Factory._SAFE_MODULES
            )
            return generador_clase(ejercicio)
        except ImportError as e:
            raise ValueError(
                f"No se pudo cargar el generador para el ejercicio {ejercicio}: {e}"
            )
