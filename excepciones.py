import logging

# Configuración del archivo de logs para registrar eventos y errores sin detener el programa
logging.basicConfig(
    filename="sistema_fj.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

class ErrorSoftwareFJ(Exception):
    """Excepción base personalizada para todo el sistema de Software FJ."""
    pass

class DatoInvalidoError(ErrorSoftwareFJ):
    """Se lanza cuando un dato personal o parámetro no cumple con las reglas."""
    pass

class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """Se lanza cuando se intenta usar o reservar un servicio inactivo o ocupado."""
    pass

class ReservaInvalidaError(ErrorSoftwareFJ):
    """Se lanza cuando ocurre un fallo al crear, confirmar o cancelar una reserva."""
    pass
