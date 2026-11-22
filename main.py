# ==============================================================================
# MÓDULO 5: SCRIPT PRINCIPAL CON 12 SIMULACIONES COMPLETAS (VÁLIDAS E INVÁLIDAS)
# Archivo: main.py
# ==============================================================================

from src.servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada  # Importa las subclases
from src.reservas_y_gestor import GestorSoftwareFJ  # Importa el gestor principal en memoria


def ejecutar_simulaciones():
    """Ejecuta 12 escenarios completos validando POO, excepciones avanzadas y estabilidad continua."""
    gestor = GestorSoftwareFJ()  # Instancia el gestor central en memoria

    print("\n" + "=" * 85)
    print("SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS - SOFTWARE FJ")
    print("=" * 85)

    # 1. Registro VÁLIDO de clientes
    print("\n[Simulación 1] Registro válido de clientes en memoria:")
    gestor.registrar_cliente("CLI-001", "Gustavo Mauricio Guzmán", "gustavo.guzman@softwarefj.com", "3001234567")
    gestor.registrar_cliente("CLI-002", "Laura Sofía Martínez", "laura.martinez@empresa.co", "3109876543")

    # 2. Registro INVÁLIDO de cliente (Correo electrónico mal formado)
    print("\n[Simulación 2] Registro inválido de cliente (Correo sin '@' ni dominio):")
    gestor.registrar_cliente("CLI-003", "Carlos Andrés Pérez", "carlosperez_invalido.com", "3151112233")

    # 3. Registro INVÁLIDO de cliente (Teléfono con caracteres alfabéticos e ID duplicado)
    print("\n[Simulación 3] Registro inválido de cliente (Teléfono con letras e ID duplicado):")
    gestor.registrar_cliente("CLI-004", "Ana María Gómez", "ana.gomez@correo.com", "300ABC999")
    gestor.registrar_cliente("CLI-001", "Cliente Duplicado", "duplicado@correo.com", "3205554433")

    # 4. Creación VÁLIDA de los 3 tipos de servicios especializados (Polimorfismo)
    print("\n[Simulación 4] Creación válida de los 3 servicios especializados:")
    gestor.registrar_servicio(
        lambda: ReservaSala("SRV-SALA-01", "Sala Ejecutiva Norte", 80000.0, capacidad_personas=15, incluye_videobeam=True)
    )
    gestor.registrar_servicio(
        lambda: AlquilerEquipo("SRV-EQU-01", "Workstations Desarrollo", 45000.0, cantidad_equipos=4, gama="Alta")
    )
    gestor.registrar_servicio(
        lambda: AsesoriaEspecializada("SRV-ASE-01", "Consultoría Cloud & DevOps", 150000.0, especialidad="Arquitectura Cloud", nivel_consultor="Senior")
    )

    # 5. Creación VÁLIDA de un servicio marcado como NO DISPONIBLE
    print("\n[Simulación 5] Creación de sala en mantenimiento (Estado: No disponible):")
    gestor.registrar_servicio(
        lambda: ReservaSala("SRV-SALA-02", "Auditorio Principal", 200000.0, capacidad_personas=80, disponible=False)
    )

    # 6. Creación INVÁLIDA de servicio (Tarifa base negativa y gama inexistente)
    print("\n[Simulación 6] Creación inválida de servicios (Tarifa negativa / Gama no permitida):")
    gestor.registrar_servicio(
        lambda: AlquilerEquipo("SRV-EQU-ERR1", "Servidor Defectuoso", -50000.0, cantidad_equipos=2, gama="Workstation")
    )
    gestor.registrar_servicio(
        lambda: AlquilerEquipo("SRV-EQU-ERR2", "Laptop Básica", 30000.0, cantidad_equipos=1, gama="UltraMega")
    )

    # 7. Reserva EXITOSA de Sala de Juntas (con IVA y descuento)
    print("\n[Simulación 7] Reserva exitosa de Sala Ejecutiva (4 horas, IVA 19%, Descuento 10%):")
    gestor.ejecutar_flujo_reserva("RES-101", "CLI-001", "SRV-SALA-01", duracion_horas=4, impuesto_pct=19.0, descuento_pct=10.0)

    # 8. Reserva EXITOSA de Asesoría Especializada
    print("\n[Simulación 8] Reserva exitosa de Asesoría Cloud Senior (6 horas, IVA 19%, Descuento 5%):")
    gestor.ejecutar_flujo_reserva("RES-102", "CLI-002", "SRV-ASE-01", duracion_horas=6, impuesto_pct=19.0, descuento_pct=5.0)

    # 9. Reserva FALLIDA por Servicio No Disponible
    print("\n[Simulación 9] Intento de reserva sobre servicio NO disponible (Auditorio en mantenimiento):")
    gestor.ejecutar_flujo_reserva("RES-103", "CLI-001", "SRV-SALA-02", duracion_horas=3)

    # 10. Reserva FALLIDA con Encadenamiento de Excepciones (Descuento > 100%)
    print("\n[Simulación 10] Reserva con cálculo inconsistente (Descuento 150% -> Excepción Encadenada):")
    gestor.ejecutar_flujo_reserva("RES-104", "CLI-001", "SRV-EQU-01", duracion_horas=5, impuesto_pct=19.0, descuento_pct=150.0)

    # 11. Reserva FALLIDA por Operación No Permitida (Cancelar una reserva ya PROCESADA)
    print("\n[Simulación 11] Intento de cancelar una reserva que ya fue PROCESADA:")
    gestor.ejecutar_flujo_reserva("RES-105", "CLI-002", "SRV-EQU-01", duracion_horas=2, procesar_inmediatamente=True, cancelar_despues=True)

    # 12. Reserva FALLIDA por Cliente Inexistente y prueba explícita de Sobrecarga de Métodos
    print("\n[Simulación 12] Intento de reserva con cliente inexistente + Prueba de sobrecarga de costos:")
    gestor.ejecutar_flujo_reserva("RES-106", "CLI-999", "SRV-SALA-01", duracion_horas=2)

    # Demostración de las 3 variantes del método sobrecargado calcular_costo()
    servicio_demo = gestor.buscar_servicio("SRV-ASE-01")
    print("\n--- Demostración explícita del método sobrecargado calcular_costo() ---")
    print(f"  Variante 1 (Solo duración 2h): ${servicio_demo.calcular_costo(2):,.2f}")
    print(f"  Variante 2 (2h + IVA 19%): ${servicio_demo.calcular_costo(2, impuesto_pct=19.0):,.2f}")
    print(
        f"  Variante 3 (2h + IVA 19% + Desc 10% + Cargo extra $50,000): "
        f"${servicio_demo.calcular_costo(2, impuesto_pct=19.0, descuento_pct=10.0, cargo_extra=50000):,.2f}"
    )

    print("\n" + "=" * 85)
    print("EJECUCIÓN COMPLETADA SIN INTERRUPCIONES. REVISE EL ARCHIVO 'software_fj.log'.")
    print("=" * 85 + "\n")


if __name__ == "__main__":
    ejecutar_simulaciones()