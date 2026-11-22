# ==============================================================================
# MÓDULO 2: CLASE ABSTRACTA DE ENTIDAD GENERAL Y CLASE CLIENTE
# Archivo: src/base_y_clientes.py
# ==============================================================================

from abc import ABC, abstractmethod  # Importa ABC y abstractmethod para definir clases abstractas
from datetime import datetime  # Importa datetime para registrar la marca de tiempo de creación
from src.excepciones_y_logs import DatosInvalidosError  # Importa la excepción personalizada de validación


class EntidadSistema(ABC):
    """Clase abstracta general que representa cualquier entidad identificable dentro de Software FJ."""

    def __init__(self, id_entidad: str):
        # Valida que el identificador sea una cadena de texto no vacía
        if not id_entidad or not isinstance(id_entidad, str) or not id_entidad.strip():
            raise DatosInvalidosError("El ID de la entidad es obligatorio y debe ser un texto válido.")
        self._id_entidad = id_entidad.strip()  # Atributo protegido para el identificador único
        self._fecha_creacion = datetime.now()  # Almacena la fecha y hora exacta de instanciación

    @property
    def id_entidad(self) -> str:
        """Propiedad getter para consultar el ID de la entidad de manera encapsulada."""
        return self._id_entidad  # Retorna el identificador protegido

    @abstractmethod
    def validar_integridad(self) -> bool:
        """Método abstracto que obliga a las clases hijas a validar su estado interno."""
        pass  # Implementación delegada obligatoriamente a las subclases

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Método abstracto para obtener una descripción textual estructurada de la entidad."""
        pass  # Implementación delegada obligatoriamente a las subclases


class Cliente(EntidadSistema):
    """Clase que modela a un cliente con encapsulación privada (__) y validaciones en setters."""

    def __init__(self, id_cliente: str, nombre: str, email: str, telefono: str):
        super().__init__(id_cliente)  # Invoca el constructor de la clase abstracta EntidadSistema
        self.__nombre = ""  # Inicializa atributo privado para el nombre completo
        self.__email = ""  # Inicializa atributo privado para el correo electrónico
        self.__telefono = ""  # Inicializa atributo privado para el número telefónico

        # Asigna los valores mediante los setters para ejecutar automáticamente las validaciones
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.validar_integridad()  # Verifica la integridad completa de la instancia

    @property
    def nombre(self) -> str:
        """Getter encapsulado para obtener el nombre del cliente."""
        return self.__nombre  # Retorna el atributo privado __nombre

    @nombre.setter
    def nombre(self, valor: str):
        """Setter con validación estricta para el nombre del cliente."""
        if not valor or not isinstance(valor, str) or len(valor.strip()) < 3:
            raise DatosInvalidosError(
                f"Nombre de cliente inválido ('{valor}'). Debe contener al menos 3 caracteres."
            )
        self.__nombre = valor.strip()  # Asigna el nombre depurado de espacios en blanco

    @property
    def email(self) -> str:
        """Getter encapsulado para obtener el correo electrónico del cliente."""
        return self.__email  # Retorna el atributo privado __email

    @email.setter
    def email(self, valor: str):
        """Setter con validación estructural para el correo electrónico."""
        if not valor or not isinstance(valor, str) or "@" not in valor or "." not in valor.split("@")[-1]:
            raise DatosInvalidosError(
                f"Correo electrónico inválido ('{valor}'). Formato esperado: usuario@dominio.com"
            )
        self.__email = valor.strip().lower()  # Normaliza y almacena el correo en minúsculas

    @property
    def telefono(self) -> str:
        """Getter encapsulado para obtener el número de teléfono del cliente."""
        return self.__telefono  # Retorna el atributo privado __telefono

    @telefono.setter
    def telefono(self, valor: str):
        """Setter que verifica que el teléfono tenga entre 7 y 15 dígitos numéricos."""
        limpio = str(valor).strip()  # Convierte a cadena y elimina espacios extremos
        if not limpio.isdigit() or len(limpio) < 7 or len(limpio) > 15:
            raise DatosInvalidosError(
                f"Teléfono inválido ('{valor}'). Debe contener únicamente entre 7 y 15 dígitos."
            )
        self.__telefono = limpio  # Almacena el número telefónico validado

    def validar_integridad(self) -> bool:
        """Implementación del método abstracto que verifica que ningún atributo obligatorio esté vacío."""
        if not all([self.__nombre, self.__email, self.__telefono]):
            raise DatosInvalidosError("Faltan parámetros obligatorios en el registro del Cliente.")
        return True  # Confirma que la entidad Cliente es íntegra

    def obtener_resumen(self) -> str:
        """Implementación polimórfica que devuelve el resumen formateado del cliente."""
        return f"Cliente[ID={self.id_entidad}, Nombre='{self.__nombre}', Email='{self.__email}', Tel='{self.__telefono}']"