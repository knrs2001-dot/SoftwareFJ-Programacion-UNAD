from abc import ABC, abstractmethod
from excepciones import DatoInvalidoError
import logging

class EntidadSistema(ABC):
    """Clase abstracta base que representa cualquier entidad general del sistema."""
    
    def __init__(self, id_entidad: str):
        if not id_entidad or not isinstance(id_entidad, str):
            raise DatoInvalidoError("El ID de la entidad debe ser un texto no vacío.")
        self._id = id_entidad.strip()

    @property
    def id(self) -> str:
        return self._id

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Método abstracto obligatorio para describir la entidad."""
        pass


class Cliente(EntidadSistema):
    """Clase que gestiona los datos personales del cliente con encapsulación estricta."""
    
    def __init__(self, id_cliente: str, nombre: str, correo: str):
        super().__init__(id_cliente)
        # Uso de setters para validar desde la creación del objeto
        self.nombre = nombre
        self.correo = correo

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or len(valor.strip()) < 3:
            raise DatoInvalidoError(f"Nombre inválido '{valor}': debe tener al menos 3 caracteres.")
        self.__nombre = valor.strip()

    @property
    def correo(self) -> str:
        return self.__correo

    @correo.setter
    def correo(self, valor: str):
        if not valor or "@" not in valor or "." not in valor:
            raise DatoInvalidoError(f"Correo inválido '{valor}': formato incorrecto.")
        self.__correo = valor.strip()

    def obtener_resumen(self) -> str:
        return f"Cliente [{self.id}]: {self.__nombre} ({self.__correo})"
