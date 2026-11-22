# ==============================================================================
# MÓDULO 1: CONFIGURACIÓN DE LOGS Y EXCEPCIONES PERSONALIZADAS
# Archivo: src/excepciones_y_logs.py
# ==============================================================================

import logging  # Importa el módulo estándar de Python para registrar eventos y errores en archivo

# Configura el sistema de logging para escribir todos los eventos y errores en 'software_fj.log'
logging.basicConfig(
    filename="software_fj.log",  # Nombre del archivo físico donde se almacenarán los logs
    level=logging.INFO,  # Nivel mínimo de registro (captura INFO, WARNING, ERROR y CRITICAL)
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",  # Formato estructurado de cada línea
    datefmt="%Y-%m-%d %H:%M:%S",  # Formato estándar de fecha y hora
    encoding="utf-8"  # Codificación UTF-8 para soportar tildes y caracteres en español
)

# Crea la instancia principal del logger para todo el ecosistema de Software FJ
logger = logging.getLogger("SoftwareFJ")


class SoftwareFJError(Exception):
    """Clase base para todas las excepciones personalizadas del sistema Software FJ."""

    def __init__(self, mensaje: str, codigo_error: int = 500):
        super().__init__(mensaje)  # Inicializa la clase padre Exception con el mensaje descriptivo
        self.mensaje = mensaje  # Almacena el mensaje de error como atributo accesible
        self.codigo_error = codigo_error  # Asigna un código numérico identificador del tipo de fallo


class DatosInvalidosError(SoftwareFJError):
    """Excepción lanzada cuando los datos de entrada o parámetros son inválidos o faltantes."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error=400)  # Código 400: Error de validación de datos


class ServicioNoDisponibleError(SoftwareFJError):
    """Excepción lanzada cuando se intenta reservar un servicio inactivo o sin capacidad."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error=409)  # Código 409: Conflicto de disponibilidad


class CalculoInconsistenteError(SoftwareFJError):
    """Excepción lanzada cuando ocurre una inconsistencia matemática en tarifas, descuentos o impuestos."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error=422)  # Código 422: Error en cálculo financiero


class OperacionReservaError(SoftwareFJError):
    """Excepción lanzada cuando falla el procesamiento, confirmación o cancelación de una reserva."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error=500)  # Código 500: Error en el ciclo de vida de la reserva