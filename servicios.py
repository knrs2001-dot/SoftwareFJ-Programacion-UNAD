from abc import abstractmethod
from modelos_base import EntidadSistema
from excepciones import DatoInvalidoError, ServicioNoDisponibleError

class Servicio(EntidadSistema):
    """Clase abstracta especializada para los servicios ofrecidos por Software FJ."""
    
    def __init__(self, id_servicio: str, nombre_servicio: str, tarifa_base: float, disponible: bool = True):
        super().__init__(id_servicio)
        if not nombre_servicio:
            raise DatoInvalidoError("El nombre del servicio no puede estar vacío.")
        if tarifa_base <= 0:
            raise DatoInvalidoError("La tarifa base debe ser mayor a cero.")
        
        self._nombre_servicio = nombre_servicio
        self._tarifa_base = float(tarifa_base)
        self._disponible = disponible

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool):
        self._disponible = estado

    @abstractmethod
    def validar_parametros(self, horas: int) -> None:
        """Valida reglas específicas según el tipo de servicio."""
        pass

    @abstractmethod
    def calcular_costo(self, horas: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        """Método polimórfico con parámetros opcionales (sobrecarga) para calcular costos."""
        pass


class ReservaSala(Servicio):
    """Servicio especializado para alquiler de salas de juntas o capacitación."""
    
    def __init__(self, id_servicio: str, nombre_servicio: str, tarifa_base: float, capacidad: int):
        super().__init__(id_servicio, nombre_servicio, tarifa_base)
        if capacidad <= 0:
            raise DatoInvalidoError("La capacidad de la sala debe ser positiva.")
        self.capacidad = capacidad

    def validar_parametros(self, horas: int) -> None:
        if not self.disponible:
            raise ServicioNoDisponibleError(f"La sala '{self._nombre_servicio}' no está disponible.")
        if horas < 1 or horas > 12:
            raise DatoInvalidoError("Las salas se reservan entre 1 y 12 horas máximo.")

    def calcular_costo(self, horas: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        self.validar_parametros(horas)
        subtotal = self._tarifa_base * horas
        subtotal_con_desc = subtotal * (1 - descuento)
        return round(subtotal_con_desc * (1 + impuesto), 2)

    def obtener_resumen(self) -> str:
        return f"Sala [{self.id}]: {self._nombre_servicio} (Cap: {self.capacidad} pers.) - ${self._tarifa_base}/h"


class AlquilerEquipo(Servicio):
    """Servicio especializado para préstamo de hardware y equipos de cómputo."""
    
    def __init__(self, id_servicio: str, nombre_servicio: str, tarifa_base: float, gama: str):
        super().__init__(id_servicio, nombre_servicio, tarifa_base)
        self.gama = gama

    def validar_parametros(self, horas: int) -> None:
        if not self.disponible:
            raise ServicioNoDisponibleError(f"El equipo '{self._nombre_servicio}' está en mantenimiento.")
        if horas < 2:
            raise DatoInvalidoError("El alquiler mínimo de equipos es de 2 horas.")

    def calcular_costo(self, horas: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        self.validar_parametros(horas)
        # Incluye seguro obligatorio de $10.000 por alquiler de equipo
        subtotal = (self._tarifa_base * horas) + 10000
        subtotal_con_desc = subtotal * (1 - descuento)
        return round(subtotal_con_desc * (1 + impuesto), 2)

    def obtener_resumen(self) -> str:
        return f"Equipo [{self.id}]: {self._nombre_servicio} (Gama {self.gama}) - ${self._tarifa_base}/h"


class AsesoriaEspecializada(Servicio):
    """Servicio especializado para consultoría técnica de ingeniería."""
    
    def __init__(self, id_servicio: str, nombre_servicio: str, tarifa_base: float, especialidad: str):
        super().__init__(id_servicio, nombre_servicio, tarifa_base)
        self.especialidad = especialidad

    def validar_parametros(self, horas: int) -> None:
        if not self.disponible:
            raise ServicioNoDisponibleError(f"El consultor de '{self.especialidad}' no tiene agenda.")
        if horas <= 0:
            raise DatoInvalidoError("La duración de la asesoría debe ser mayor a 0 horas.")

    def calcular_costo(self, horas: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        self.validar_parametros(horas)
        subtotal = self._tarifa_base * horas
        # Si son más de 5 horas, aplica bono automático del 5% adicional
        if horas > 5:
            descuento += 0.05
        subtotal_con_desc = subtotal * (1 - min(descuento, 0.5))
        return round(subtotal_con_desc * (1 + impuesto), 2)

    def obtener_resumen(self) -> str:
        return f"Asesoría [{self.id}]: {self._nombre_servicio} ({self.especialidad}) - ${self._tarifa_base}/h"
