import logging
from modelos_base import EntidadSistema, Cliente
from servicios import Servicio
from excepciones import ReservaInvalidaError, DatoInvalidoError, ErrorSoftwareFJ

class Reserva(EntidadSistema):
    """Clase que integra cliente, servicio, duración y estado de una reserva."""

    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, horas: int):
        super().__init__(id_reserva)
        
        if not isinstance(cliente, Cliente):
            raise DatoInvalidoError("Se requiere un objeto Cliente válido.")
        if not isinstance(servicio, Servicio):
            raise DatoInvalidoError("Se requiere un objeto Servicio válido.")
        if horas <= 0:
            raise DatoInvalidoError("Las horas de reserva deben ser mayores a cero.")

        self.cliente = cliente
        self.servicio = servicio
        self.horas = horas
        self.estado = "PENDIENTE"
        self.costo_total = 0.0

    def procesar_y_confirmar(self, descuento: float = 0.0) -> None:
        """Calcula el costo usando polimorfismo y confirma la reserva con manejo avanzado de errores."""
        try:
            if self.estado == "CANCELADA":
                raise ReservaInvalidaError("No se puede confirmar una reserva que ya fue cancelada.")
            
            # Intenta calcular el costo llamando al método polimórfico del servicio
            self.costo_total = self.servicio.calcular_costo(self.horas, descuento=descuento)
            
        except ErrorSoftwareFJ as error_origen:
            # Encadenamiento de excepciones exigido en la guía
            logging.error(f"Fallo al procesar reserva {self.id}: {error_origen}")
            raise ReservaInvalidaError(f"Error en la reserva {self.id} para {self.cliente.nombre}") from error_origen
        else:
            # Bloque else: solo se ejecuta si no hubo errores en el try
            self.estado = "CONFIRMADA"
            self.servicio.disponible = False
            logging.info(f"Reserva {self.id} CONFIRMADA. Total: ${self.costo_total}")
        finally:
            # Bloque finally: siempre se ejecuta para dejar traza en el log
            logging.info(f"Fin de intento de procesamiento para reserva {self.id} (Estado actual: {self.estado}).")

    def cancelar(self) -> None:
        """Cancela la reserva y libera el servicio."""
        if self.estado == "CANCELADA":
            raise ReservaInvalidaError(f"La reserva {self.id} ya se encuentra cancelada.")
        
        self.estado = "CANCELADA"
        self.servicio.disponible = True
        logging.warning(f"Reserva {self.id} fue CANCELADA por el usuario.")

    def obtener_resumen(self) -> str:
        return (f"Reserva [{self.id}] | Estado: {self.estado} | "
                f"{self.cliente.nombre} -> {self.servicio._nombre_servicio} ({self.horas}h) | Total: ${self.costo_total}")
