# ==============================================================================
# MÓDULO 4: CLASE RESERVA Y GESTOR CENTRAL EN MEMORIA (SIN BASE DE DATOS)
# Archivo: src/reservas_y_gestor.py
# ==============================================================================

from typing import Callable, List, Optional  # Importa tipos para colecciones y funciones constructoras
from src.base_y_clientes import EntidadSistema, Cliente  # Importa clase base y Cliente
from src.servicios import Servicio  # Importa clase abstracta Servicio
from src.excepciones_y_logs import (  # Importa el logger y todas las excepciones personalizadas
    logger,
    SoftwareFJError,
    DatosInvalidosError,
    ServicioNoDisponibleError,
    CalculoInconsistenteError,
    OperacionReservaError,
)


class Reserva(EntidadSistema):
    """Clase que integra Cliente, Servicio, duración y estado, gestionando su ciclo de vida."""

    ESTADOS_PERMITIDOS = ("PENDIENTE", "CONFIRMADA", "PROCESADA", "CANCELADA")

    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion_horas: float):
        super().__init__(id_reserva)  # Inicializa el identificador en EntidadSistema
        self._cliente = cliente  # Asocia la instancia de Cliente
        self._servicio = servicio  # Asocia la instancia de Servicio
        self._duracion_horas = duracion_horas  # Almacena la duración solicitada en horas
        self._estado = "PENDIENTE"  # Estado inicial al crearse la reserva
        self._costo_total = 0.0  # Valor financiero calculado al confirmar
        self.validar_integridad()  # Ejecuta validaciones estructurales iniciales

    def validar_integridad(self) -> bool:
        """Verifica que el cliente y el servicio sean objetos válidos y la duración sea positiva."""
        if not isinstance(self._cliente, Cliente):
            raise DatosInvalidosError("La reserva requiere una instancia válida de la clase Cliente.")
        if not isinstance(self._servicio, Servicio):
            raise DatosInvalidosError("La reserva requiere una instancia válida de la clase Servicio.")
        if not isinstance(self._duracion_horas, (int, float)) or self._duracion_horas <= 0:
            raise DatosInvalidosError(
                f"La duración de la reserva ({self._duracion_horas}) debe ser mayor a cero horas."
            )
        return True

    def confirmar(self, impuesto_pct: float = 19.0, descuento_pct: float = 0.0):
        """Confirma la reserva verificando disponibilidad y aplicando encadenamiento de excepciones."""
        if self._estado == "CANCELADA":
            raise OperacionReservaError(
                f"No se puede confirmar la reserva '{self.id_entidad}' porque ya fue CANCELADA."
            )
        if not self._servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{self._servicio.id_entidad}' no se encuentra disponible para reservas."
            )

        try:
            # Invoca el método sobrecargado calcular_costo() del servicio
            self._costo_total = self._servicio.calcular_costo(
                self._duracion_horas,
                impuesto_pct=impuesto_pct,
                descuento_pct=descuento_pct
            )
        except CalculoInconsistenteError as error_calculo:
            # ENCADENAMIENTO DE EXCEPCIONES (raise ... from ...) exigido por la rúbrica
            raise OperacionReservaError(
                f"Fallo al confirmar la reserva '{self.id_entidad}' debido a una inconsistencia financiera."
            ) from error_calculo
        else:
            # Bloque ELSE: Solo se ejecuta si el cálculo de costos no arrojó ninguna excepción
            self._estado = "CONFIRMADA"
            logger.info(
                f"Reserva '{self.id_entidad}' CONFIRMADA para '{self._cliente.nombre}'. Total: ${self._costo_total:,.2f}"
            )

    def procesar(self):
        """Ejecuta y finaliza una reserva que haya sido previamente confirmada."""
        if self._estado != "CONFIRMADA":
            raise OperacionReservaError(
                f"Operación no permitida: la reserva '{self.id_entidad}' debe estar CONFIRMADA para procesarse "
                f"(estado actual: {self._estado})."
            )
        self._estado = "PROCESADA"  # Cambia estado a procesada
        logger.info(f"Reserva '{self.id_entidad}' PROCESADA satisfactoriamente.")

    def cancelar(self, motivo: str = "Solicitud del cliente"):
        """Cancela la reserva siempre que aún no haya sido procesada."""
        if self._estado == "PROCESADA":
            raise OperacionReservaError(
                f"Operación denegada: no se puede cancelar la reserva '{self.id_entidad}' porque ya está PROCESADA."
            )
        self._estado = "CANCELADA"  # Cambia estado a cancelada
        logger.warning(f"Reserva '{self.id_entidad}' CANCELADA. Motivo: {motivo}")

    def obtener_resumen(self) -> str:
        """Retorna una cadena descriptiva con los datos completos de la reserva."""
        return (
            f"Reserva[ID={self.id_entidad}, Cliente='{self._cliente.nombre}', "
            f"Servicio='{self._servicio.id_entidad}', Horas={self._duracion_horas}, "
            f"Estado={self._estado}, CostoTotal=${self._costo_total:,.2f}]"
        )


class GestorSoftwareFJ:
    """Controlador principal que administra las listas en memoria sin utilizar bases de datos."""

    def __init__(self):
        self._clientes: List[Cliente] = []  # Lista interna en memoria para objetos Cliente
        self._servicios: List[Servicio] = []  # Lista interna en memoria para objetos Servicio
        self._reservas: List[Reserva] = []  # Lista interna en memoria para objetos Reserva
        logger.info("======================================================================")
        logger.info("INICIO DE EJECUCIÓN: Sistema Integral Software FJ (Sin Base de Datos)")
        logger.info("======================================================================")

    def registrar_cliente(self, id_cliente: str, nombre: str, email: str, telefono: str) -> Optional[Cliente]:
        """Registra un cliente utilizando bloques try/except/else/finally para garantizar continuidad."""
        exito = False  # Bandera de auditoría para el bloque finally
        try:
            # Verifica que no exista un cliente con el mismo ID en la lista interna
            if any(c.id_entidad == id_cliente for c in self._clientes):
                raise DatosInvalidosError(f"El ID de cliente '{id_cliente}' ya se encuentra registrado.")
            nuevo_cliente = Cliente(id_cliente, nombre, email, telefono)  # Crea y valida el cliente
        except SoftwareFJError as e:
            # Captura errores de validación, los registra en el log y evita que el sistema colapse
            logger.error(f"[ERROR CLIENTE] Código {e.codigo_error}: {e.mensaje}")
            print(f"  [!] Error controlado al registrar cliente '{id_cliente}': {e.mensaje}")
            return None
        else:
            # Bloque ELSE: Se ejecuta únicamente si el cliente fue creado sin excepciones
            self._clientes.append(nuevo_cliente)  # Almacena el objeto en la lista interna
            exito = True
            logger.info(f"[CLIENTE REGISTRADO] {nuevo_cliente.obtener_resumen()}")
            print(f"  [OK] {nuevo_cliente.obtener_resumen()}")
            return nuevo_cliente
        finally:
            # Bloque FINALLY: Se ejecuta siempre para dejar trazabilidad de auditoría
            estado = "EXITOSO" if exito else "FALLIDO"
            logger.info(f"[FINALLY AUDITORÍA] Intento de registro de cliente '{id_cliente}' finalizado -> {estado}.")

    def registrar_servicio(self, constructor_servicio: Callable[[], Servicio]) -> Optional[Servicio]:
        """Instancia y registra un servicio especializado capturando cualquier error de parámetros."""
        try:
            nuevo_servicio = constructor_servicio()  # Ejecuta la función constructora del servicio
            if any(s.id_entidad == nuevo_servicio.id_entidad for s in self._servicios):
                raise DatosInvalidosError(f"El ID de servicio '{nuevo_servicio.id_entidad}' ya existe.")
        except SoftwareFJError as e:
            logger.error(f"[ERROR SERVICIO] Código {e.codigo_error}: {e.mensaje}")
            print(f"  [!] Error controlado al registrar servicio: {e.mensaje}")
            return None
        else:
            self._servicios.append(nuevo_servicio)  # Agrega el servicio a la lista en memoria
            logger.info(f"[SERVICIO REGISTRADO] {nuevo_servicio.describir_servicio()}")
            print(f"  [OK] {nuevo_servicio.describir_servicio()}")
            return nuevo_servicio

    def buscar_cliente(self, id_cliente: str) -> Cliente:
        """Busca un cliente por ID en la lista interna o lanza DatosInvalidosError."""
        for cliente in self._clientes:
            if cliente.id_entidad == id_cliente:
                return cliente
        raise DatosInvalidosError(f"No existe ningún cliente registrado con el ID '{id_cliente}'.")

    def buscar_servicio(self, id_servicio: str) -> Servicio:
        """Busca un servicio por ID en la lista interna o lanza DatosInvalidosError."""
        for servicio in self._servicios:
            if servicio.id_entidad == id_servicio:
                return servicio
        raise DatosInvalidosError(f"No existe ningún servicio registrado con el ID '{id_servicio}'.")

    def ejecutar_flujo_reserva(
        self,
        id_reserva: str,
        id_cliente: str,
        id_servicio: str,
        duracion_horas: float,
        impuesto_pct: float = 19.0,
        descuento_pct: float = 0.0,
        procesar_inmediatamente: bool = True,
        cancelar_despues: bool = False
    ) -> Optional[Reserva]:
        """Orquesta la creación, confirmación, procesamiento y cancelación de reservas sin detener el sistema."""
        try:
            cliente = self.buscar_cliente(id_cliente)  # Obtiene el objeto Cliente de memoria
            servicio = self.buscar_servicio(id_servicio)  # Obtiene el objeto Servicio de memoria
            reserva = Reserva(id_reserva, cliente, servicio, duracion_horas)  # Crea la reserva
            reserva.confirmar(impuesto_pct=impuesto_pct, descuento_pct=descuento_pct)  # Confirma y calcula costos

            if procesar_inmediatamente:
                reserva.procesar()  # Cambia el estado a PROCESADA
            if cancelar_despues:
                reserva.cancelar("Prueba de cancelación posterior")  # Ejecuta intento de cancelación
        except SoftwareFJError as e:
            # Si existe una excepción encadenada (__cause__), extrae su detalle para el log
            detalle_causa = f" | Causa encadenada: {e.__cause__}" if e.__cause__ else ""
            logger.error(f"[ERROR RESERVA '{id_reserva}'] Código {e.codigo_error}: {e.mensaje}{detalle_causa}")
            print(f"  [!] Excepción controlada en reserva '{id_reserva}': {e.mensaje}{detalle_causa}")
            return None
        else:
            self._reservas.append(reserva)  # Guarda la reserva exitosa en la lista interna
            print(f"  [OK] {reserva.obtener_resumen()}")
            return reserva
        finally:
            logger.info(f"[FINALLY RESERVA] Transacción de reserva '{id_reserva}' finalizada.")