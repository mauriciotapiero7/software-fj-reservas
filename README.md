# software-fj-reservas
software-fj-reservas proyect


# Sistema Integral de Gestión de Clientes, Servicios y Reservas — Software FJ

**Curso:** Programación (Código: 213023) — Universidad Nacional Abierta y a Distancia (UNAD)  
**Actividad:** Fase 4 — Componente Práctico (Prácticas Simuladas)  
**Repositorio:** [https://github.com/mauriciotapiero7/software-fj-reservas](https://github.com/mauriciotapiero7/software-fj-reservas)

---

## 1. Descripción General
Aplicación desarrollada en **Python 3** bajo el paradigma de **Programación Orientada a Objetos (POO)** sin uso de bases de datos. Toda la gestión de datos se realiza en memoria mediante estructuras de objetos y listas internas, garantizando la persistencia de eventos y auditoría de errores en un archivo plano de registros (`software_fj.log`).

### Principios y Requisitos Implementados
* **Abstracción:** Clases abstractas `EntidadSistema` y `Servicio` implementadas mediante el módulo estándar `abc`.
* **Encapsulación:** Protección de atributos sensibles en `Cliente` (`__nombre`, `__email`, `__telefono`) con validación estricta en decoradores `@property` y `@setter`.
* **Herencia y Polimorfismo:** Especialización de tres servicios concretos (`ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada`) con sobrescritura de `calcular_costo_base()`, `describir_servicio()` y `validar_parametros()`.
* **Sobrecarga de Métodos:** Implementada en `Servicio.calcular_costo()` soportando múltiples combinaciones de parámetros opcionales (duración base, impuestos porcentuales, descuentos y cargos adicionales).
* **Manejo Avanzado de Excepciones:** Jerarquía de excepciones personalizadas (`SoftwareFJError`, `DatosInvalidosError`, `ServicioNoDisponibleError`, `CalculoInconsistenteError`, `OperacionReservaError`), bloques `try/except`, `try/except/else`, `try/except/finally` y **encadenamiento de excepciones** (`raise ... from ...`).

---

## 2. Arquitectura del Proyecto (Diagrama de Clases UML)

```mermaid
classDiagram
    class EntidadSistema {
        <<abstract>>
        #_id_entidad: str
        #_fecha_creacion: datetime
        +validar_integridad()* bool
        +obtener_resumen()* str
    }
    class Cliente {
        -__nombre: str
        -__email: str
        -__telefono: str
        +validar_integridad() bool
        +obtener_resumen() str
    }
    class Servicio {
        <<abstract>>
        #_nombre_servicio: str
        #_tarifa_base_hora: float
        #_disponible: bool
        +calcular_costo_base(duracion)* float
        +describir_servicio()* str
        +validar_parametros()* bool
        +calcular_costo(duracion, impuesto, descuento, cargo_extra) float
    }
    class ReservaSala {
        -_capacidad_personas: int
        -_incluye_videobeam: bool
    }
    class AlquilerEquipo {
        -_cantidad_equipos: int
        -_gama: str
    }
    class AsesoriaEspecializada {
        -_especialidad: str
        -_nivel_consultor: str
    }
    class Reserva {
        -_cliente: Cliente
        -_servicio: Servicio
        -_duracion_horas: float
        -_estado: str
        -_costo_total: float
        +confirmar(impuesto, descuento)
        +procesar()
        +cancelar(motivo)
    }

    EntidadSistema <|-- Cliente
    EntidadSistema <|-- Servicio
    EntidadSistema <|-- Reserva
    Servicio <|-- ReservaSala
    Servicio <|-- AlquilerEquipo
    Servicio <|-- AsesoriaEspecializada
    Reserva --> Cliente
    Reserva --> Servicio