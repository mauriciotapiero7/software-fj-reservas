# ==============================================================================
# MÓDULO 3: CLASE ABSTRACTA SERVICIO Y TRES SERVICIOS ESPECIALIZADOS
# Archivo: src/servicios.py
# ==============================================================================

from abc import abstractmethod  # Importa abstractmethod para definir contratos polimórficos
from typing import Optional  # Importa Optional para tipar los parámetros opcionales de sobrecarga
from src.base_y_clientes import EntidadSistema  # Importa la clase base abstracta del sistema
from src.excepciones_y_logs import DatosInvalidosError, CalculoInconsistenteError  # Importa excepciones


class Servicio(EntidadSistema):
    """Clase abstracta Servicio que define el contrato polimórfico y la sobrecarga de costos."""

    def __init__(self, id_servicio: str, nombre_servicio: str, tarifa_base_hora: float, disponible: bool = True):
        super().__init__(id_servicio)  # Llama al constructor de EntidadSistema para validar el ID
        if not nombre_servicio or not isinstance(nombre_servicio, str):
            raise DatosInvalidosError("El nombre del servicio es obligatorio.")
        if not isinstance(tarifa_base_hora, (int, float)) or tarifa_base_hora <= 0:
            raise CalculoInconsistenteError(
                f"La tarifa base por hora ({tarifa_base_hora}) debe ser un valor positivo mayor a cero."
            )
        self._nombre_servicio = nombre_servicio.strip()  # Nombre comercial del servicio
        self._tarifa_base_hora = float(tarifa_base_hora)  # Tarifa base expresada en pesos por hora
        self._disponible = bool(disponible)  # Bandera booleana de disponibilidad del servicio

    @property
    def disponible(self) -> bool:
        """Getter que indica si el servicio se encuentra disponible para ser reservado."""
        return self._disponible  # Retorna el estado booleano actual

    @disponible.setter
    def disponible(self, estado: bool):
        """Setter para habilitar o deshabilitar la disponibilidad del servicio."""
        self._disponible = bool(estado)  # Actualiza el estado de disponibilidad

    @abstractmethod
    def calcular_costo_base(self, duracion_horas: float) -> float:
        """Método abstracto sobrescrito por cada subclase según sus reglas de negocio."""
        pass

    @abstractmethod
    def describir_servicio(self) -> str:
        """Método abstracto sobrescrito por cada subclase para describir sus atributos específicos."""
        pass

    @abstractmethod
    def validar_parametros(self) -> bool:
        """Método abstracto sobrescrito por cada subclase para validar sus parámetros propios."""
        pass

    # --- SOBRECARGA DE MÉTODOS (Múltiples variantes de cálculo con impuestos, descuentos y cargos) ---
    def calcular_costo(
        self,
        duracion_horas: float,
        impuesto_pct: Optional[float] = None,
        descuento_pct: Optional[float] = None,
        cargo_extra: Optional[float] = None
    ) -> float:
        """
        Método sobrecargado para calcular el costo final de un servicio en diferentes escenarios:
        1. calcular_costo(horas) -> Calcula únicamente el costo base polimórfico.
        2. calcular_costo(horas, impuesto_pct=19.0) -> Aplica IVA o impuesto porcentual.
        3. calcular_costo(horas, impuesto_pct=19.0, descuento_pct=10.0, cargo_extra=50000) -> Cálculo integral.
        """
        if not isinstance(duracion_horas, (int, float)) or duracion_horas <= 0:
            raise CalculoInconsistenteError(f"La duración ({duracion_horas} h) debe ser mayor a cero.")

        # Invoca el cálculo base polimórfico correspondiente a la subclase concreta
        subtotal = self.calcular_costo_base(duracion_horas)

        # Aplica descuento si fue proporcionado y valida que esté entre 0% y 100%
        if descuento_pct is not None:
            if not (0 <= descuento_pct <= 100):
                raise CalculoInconsistenteError(f"Porcentaje de descuento inconsistente: {descuento_pct}%.")
            subtotal -= subtotal * (descuento_pct / 100.0)

        # Aplica impuesto si fue proporcionado y valida que sea coherente
        if impuesto_pct is not None:
            if not (0 <= impuesto_pct <= 100):
                raise CalculoInconsistenteError(f"Porcentaje de impuesto inconsistente: {impuesto_pct}%.")
            subtotal += subtotal * (impuesto_pct / 100.0)

        # Suma cargo extra fijo si fue proporcionado y no es negativo
        if cargo_extra is not None:
            if cargo_extra < 0:
                raise CalculoInconsistenteError(f"El cargo adicional ({cargo_extra}) no puede ser negativo.")
            subtotal += cargo_extra

        return round(subtotal, 2)  # Retorna el monto total redondeado a dos decimales

    def validar_integridad(self) -> bool:
        """Implementación del contrato de EntidadSistema delegando en validar_parametros()."""
        return self.validar_parametros()

    def obtener_resumen(self) -> str:
        """Implementación del contrato de EntidadSistema delegando en describir_servicio()."""
        return self.describir_servicio()


class ReservaSala(Servicio):
    """Servicio especializado 1: Reserva de salas físicas para juntas, eventos o capacitación."""

    def __init__(
        self,
        id_servicio: str,
        nombre_servicio: str,
        tarifa_base_hora: float,
        capacidad_personas: int,
        incluye_videobeam: bool = True,
        disponible: bool = True
    ):
        super().__init__(id_servicio, nombre_servicio, tarifa_base_hora, disponible)  # Constructor padre
        self._capacidad_personas = capacidad_personas  # Aforo máximo permitido en la sala
        self._incluye_videobeam = bool(incluye_videobeam)  # Indica si incluye equipamiento audiovisual
        self.validar_parametros()  # Ejecuta validación específica de la sala

    def validar_parametros(self) -> bool:
        """Valida que la capacidad de personas de la sala sea un número entero positivo."""
        if not isinstance(self._capacidad_personas, int) or self._capacidad_personas <= 0:
            raise DatosInvalidosError(
                f"La capacidad de la sala ({self._capacidad_personas}) debe ser un entero mayor a cero."
            )
        return True

    def calcular_costo_base(self, duracion_horas: float) -> float:
        """Sobrescribe el cálculo: aplica un incremento del 15% si la sala incluye videobeam."""
        costo = self._tarifa_base_hora * duracion_horas  # Costo base por horas reservadas
        if self._incluye_videobeam:
            costo *= 1.15  # Recargo del 15% por soporte audiovisual
        return costo

    def describir_servicio(self) -> str:
        """Sobrescribe la descripción detallando aforo y disponibilidad de videobeam."""
        vb = "Sí" if self._incluye_videobeam else "No"
        return (
            f"ServicioSala[ID={self.id_entidad}, Sala='{self._nombre_servicio}', "
            f"Capacidad={self._capacidad_personas} pers, Videobeam={vb}, Tarifa/h=${self._tarifa_base_hora:,.2f}]"
        )


class AlquilerEquipo(Servicio):
    """Servicio especializado 2: Alquiler de hardware, estaciones de trabajo y servidores."""

    def __init__(
        self,
        id_servicio: str,
        nombre_servicio: str,
        tarifa_base_hora: float,
        cantidad_equipos: int,
        gama: str = "Alta",
        disponible: bool = True
    ):
        super().__init__(id_servicio, nombre_servicio, tarifa_base_hora, disponible)  # Constructor padre
        self._cantidad_equipos = cantidad_equipos  # Número de equipos incluidos en el paquete
        self._gama = gama  # Clasificación técnica del hardware (Media, Alta, Workstation)
        self.validar_parametros()  # Valida los atributos específicos del alquiler

    def validar_parametros(self) -> bool:
        """Valida que la cantidad de equipos sea positiva y la gama sea reconocida."""
        if not isinstance(self._cantidad_equipos, int) or self._cantidad_equipos <= 0:
            raise DatosInvalidosError(
                f"La cantidad de equipos ({self._cantidad_equipos}) debe ser un entero positivo."
            )
        if self._gama not in ("Media", "Alta", "Workstation"):
            raise DatosInvalidosError(
                f"Gama '{self._gama}' inválida. Opciones permitidas: Media, Alta o Workstation."
            )
        return True

    def calcular_costo_base(self, duracion_horas: float) -> float:
        """Sobrescribe el cálculo multiplicando por cantidad de equipos y factor de gama."""
        factores_gama = {"Media": 1.0, "Alta": 1.25, "Workstation": 1.60}  # Multiplicadores según potencia
        return self._tarifa_base_hora * duracion_horas * self._cantidad_equipos * factores_gama[self._gama]

    def describir_servicio(self) -> str:
        """Sobrescribe la descripción detallando cantidad y gama de los equipos."""
        return (
            f"ServicioEquipo[ID={self.id_entidad}, Equipo='{self._nombre_servicio}', "
            f"Cantidad={self._cantidad_equipos}, Gama={self._gama}, Tarifa/h=${self._tarifa_base_hora:,.2f}]"
        )


class AsesoriaEspecializada(Servicio):
    """Servicio especializado 3: Consultoría técnica en desarrollo de software, nube y arquitectura."""

    def __init__(
        self,
        id_servicio: str,
        nombre_servicio: str,
        tarifa_base_hora: float,
        especialidad: str,
        nivel_consultor: str = "Senior",
        disponible: bool = True
    ):
        super().__init__(id_servicio, nombre_servicio, tarifa_base_hora, disponible)  # Constructor padre
        self._especialidad = especialidad  # Área de conocimiento de la consultoría
        self._nivel_consultor = nivel_consultor  # Experiencia del consultor asignado
        self.validar_parametros()  # Valida especialidad y nivel

    def validar_parametros(self) -> bool:
        """Valida que la especialidad exista y que el nivel del consultor esté permitido."""
        if not self._especialidad or not isinstance(self._especialidad, str) or not self._especialidad.strip():
            raise DatosInvalidosError("La especialidad de la asesoría no puede estar vacía.")
        if self._nivel_consultor not in ("Junior", "SemiSenior", "Senior"):
            raise DatosInvalidosError(
                f"Nivel de consultor '{self._nivel_consultor}' no válido. Use: Junior, SemiSenior o Senior."
            )
        return True

    def calcular_costo_base(self, duracion_horas: float) -> float:
        """Sobrescribe el cálculo aplicando un factor multiplicador según el seniority."""
        multiplicadores = {"Junior": 1.0, "SemiSenior": 1.30, "Senior": 1.75}  # Factor por experiencia
        return self._tarifa_base_hora * duracion_horas * multiplicadores[self._nivel_consultor]

    def describir_servicio(self) -> str:
        """Sobrescribe la descripción detallando área técnica y nivel del consultor."""
        return (
            f"ServicioAsesoria[ID={self.id_entidad}, Especialidad='{self._especialidad}', "
            f"Nivel={self._nivel_consultor}, Tarifa/h=${self._tarifa_base_hora:,.2f}]"
        )