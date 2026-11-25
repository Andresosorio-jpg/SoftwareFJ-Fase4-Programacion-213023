"""
main.py
Autor: Andrés Felipe Osorio Suarez
Copyright (c) 2026 Andrés Felipe Osorio Suarez. Todos los derechos reservados.
Simulación de operaciones del Sistema Integral de Gestión de Clientes,
Servicios y Reservas de Software FJ.
Curso: Programación (213023) - UNAD - Fase 4 - Prácticas simuladas.

Ejecutar con:  python main.py
Los eventos y errores quedan registrados en software_fj.log
"""

from sistema import SistemaSoftwareFJ                       # Gestor central
from servicios import ReservaSala, AlquilerEquipo, Asesoria # Servicios especializados
from registro_logs import obtener_logger, ARCHIVO_LOG       # Logger y nombre del archivo

# Logger principal
log = obtener_logger()


def titulo(texto):
    """Imprime un encabezado para separar cada operación."""
    # Muestra el texto entre líneas
    print(f"\n{'=' * 70}\n{texto}\n{'=' * 70}")


def main():
    # Marca en el log el inicio de la simulación
    log.info("===== INICIO DE LA SIMULACIÓN SOFTWARE FJ =====")
    # Crea el sistema con sus listas vacías
    sistema = SistemaSoftwareFJ()

    # ---------------- Operación 1: clientes válidos ----------------
    titulo("Operación 1: registro de clientes válidos")
    # Registra tres clientes con datos correctos
    ana = sistema.ejecutar("Registrar a Ana Gómez", sistema.registrar_cliente,
                           "Ana Gómez", "1023456789", "ana.gomez@correo.com", "3104567890")
    luis = sistema.ejecutar("Registrar a Luis Pérez", sistema.registrar_cliente,
                            "Luis Pérez", "79856412", "luis.perez@empresa.co")
    marta = sistema.ejecutar("Registrar a Marta Ríos", sistema.registrar_cliente,
                             "Marta Ríos", "52987456", "marta@correo.com", "3001234567")

    # ---------------- Operación 2: clientes inválidos ----------------
    titulo("Operación 2: registro de clientes inválidos")
    # Correo sin @
    sistema.ejecutar("Cliente con correo inválido", sistema.registrar_cliente,
                     "Pedro Ruiz", "1234567", "pedro.correo.com")
    # Documento con letras
    sistema.ejecutar("Cliente con documento inválido", sistema.registrar_cliente,
                     "Laura Díaz", "ABC123", "laura@correo.com")
    # Nombre vacío (parámetro faltante)
    sistema.ejecutar("Cliente sin nombre", sistema.registrar_cliente,
                     "", "998877665", "x@correo.com")
    # Documento repetido
    sistema.ejecutar("Cliente con documento duplicado", sistema.registrar_cliente,
                     "Ana Duplicada", "1023456789", "otra@correo.com")

    # ---------------- Operación 3: servicios válidos ----------------
    titulo("Operación 3: creación correcta de servicios")
    # Crea un servicio de cada tipo
    sala = sistema.ejecutar("Crear sala de juntas", sistema.agregar_servicio,
                            ReservaSala, "Sala Juntas A", 80000, capacidad=12)
    auditorio = sistema.ejecutar("Crear auditorio", sistema.agregar_servicio,
                                 ReservaSala, "Auditorio", 250000, capacidad=120)
    portatil = sistema.ejecutar("Crear alquiler de portátiles", sistema.agregar_servicio,
                                AlquilerEquipo, "Portátil i7", 45000, unidades=3)
    asesoria = sistema.ejecutar("Crear asesoría senior", sistema.agregar_servicio,
                                Asesoria, "Arquitectura de software", 120000, nivel="senior")

    # ---------------- Operación 4: servicios inválidos ----------------
    titulo("Operación 4: creación incorrecta de servicios")
    # Tarifa negativa
    sistema.ejecutar("Servicio con tarifa negativa", sistema.agregar_servicio,
                     ReservaSala, "Sala B", -5000, capacidad=10)
    # Nivel de asesor inexistente
    sistema.ejecutar("Asesoría con nivel inexistente", sistema.agregar_servicio,
                     Asesoria, "Bases de datos", 90000, nivel="maestro")
    # Cero unidades de equipo
    sistema.ejecutar("Equipo con 0 unidades", sistema.agregar_servicio,
                     AlquilerEquipo, "Proyector", 30000, unidades=0)

    # ---------------- Operación 5: reserva exitosa completa ----------------
    titulo("Operación 5: reserva de sala exitosa (crear, confirmar, procesar con IVA)")
    r1 = sistema.ejecutar("Crear reserva sala para Ana (3 h)", sistema.crear_reserva, ana, sala, 3)
    if r1:
        # Confirma la reserva
        sistema.ejecutar("Confirmar reserva", r1.confirmar)
        # Procesa con IVA (variante con impuesto=True)
        costo = sistema.ejecutar("Procesar reserva con IVA", r1.procesar, impuesto=True)
        print(f"    Costo final: ${costo:,.2f}")

    # ---------------- Operación 6: sobrecarga del cálculo de costos ----------------
    titulo("Operación 6: variantes del cálculo de costos (sobrecarga)")
    if asesoria:
        # Sin impuesto ni descuento
        print(f"    Solo base (2 h):            ${asesoria.calcular_costo(2):,.2f}")
        # Con IVA
        print(f"    Con IVA (2 h):              ${asesoria.calcular_costo(2, impuesto=True):,.2f}")
        # Con descuento del 10 %
        print(f"    Con 10 % descuento (2 h):   ${asesoria.calcular_costo(2, descuento=0.10):,.2f}")
        # Con descuento y un impuesto diferente
        print(f"    Desc. 10 % + imp. 5 % (2 h): ${asesoria.calcular_costo(2, 0.05, 0.10):,.2f}")
        # Variante inválida: descuento del 90 %
        sistema.ejecutar("Cálculo con descuento de 90 %", asesoria.calcular_costo, 2, descuento=0.9)

    # ---------------- Operación 7: alquiler de equipos con descuento ----------------
    titulo("Operación 7: alquiler de portátiles por 7 días con descuento")
    r2 = sistema.ejecutar("Crear reserva de portátiles para Luis", sistema.crear_reserva, luis, portatil, 7)
    if r2:
        sistema.ejecutar("Confirmar reserva", r2.confirmar)
        costo = sistema.ejecutar("Procesar con 5 % de descuento e IVA", r2.procesar, True, 0.05)
        print(f"    Costo final: ${costo:,.2f}")

    # ---------------- Operación 8: reservas fallidas ----------------
    titulo("Operación 8: intentos de reserva incorrectos")
    # Duración fuera de rango para una sala (encadena DatoInvalidoError)
    sistema.ejecutar("Reserva de sala por 20 horas", sistema.crear_reserva, marta, sala, 20)
    # Días no enteros para equipos
    sistema.ejecutar("Alquiler de equipo por 2.5 días", sistema.crear_reserva, marta, portatil, 2.5)
    # Reserva sin cliente
    sistema.ejecutar("Reserva sin cliente", sistema.crear_reserva, None, sala, 2)

    # ---------------- Operación 9: servicio no disponible ----------------
    titulo("Operación 9: reserva sobre un servicio no disponible")
    if auditorio:
        # Desactiva el auditorio (por mantenimiento)
        auditorio.desactivar()
        # Intenta reservarlo (encadena ServicioNoDisponibleError)
        sistema.ejecutar("Reservar auditorio desactivado", sistema.crear_reserva, marta, auditorio, 4)

    # ---------------- Operación 10: operaciones no permitidas ----------------
    titulo("Operación 10: cancelación y operaciones no permitidas")
    r3 = sistema.ejecutar("Crear reserva de asesoría para Marta", sistema.crear_reserva, marta, asesoria, 1.5)
    if r3:
        # Procesar sin confirmar no está permitido
        sistema.ejecutar("Procesar reserva sin confirmar", r3.procesar)
        # Cancelar sí está permitido
        sistema.ejecutar("Cancelar reserva", r3.cancelar)
        # Confirmar una reserva cancelada no está permitido
        sistema.ejecutar("Confirmar reserva cancelada", r3.confirmar)
    if r1:
        # Cancelar una reserva ya procesada no está permitido
        sistema.ejecutar("Cancelar reserva ya procesada", r1.cancelar)

    # ---------------- Operación 11: error inesperado controlado ----------------
    titulo("Operación 11: error inesperado (no previsto) sin detener la aplicación")
    if sala:
        # Se pasa un texto como impuesto: genera DatoInvalidoError controlado
        r4 = sistema.ejecutar("Crear reserva de sala para Luis (2 h)", sistema.crear_reserva, luis, sala, 2)
        if r4:
            sistema.ejecutar("Confirmar reserva", r4.confirmar)
            sistema.ejecutar("Procesar con impuesto mal escrito", r4.procesar, impuesto="diecinueve")
    # División entre cero: error de Python no previsto, también se controla
    sistema.ejecutar("Operación con división entre cero", lambda: 10 / 0)

    # ---------------- Resumen final ----------------
    titulo("Resumen final: el sistema siguió funcionando")
    print(sistema.resumen())
    print(f"\nRevise el archivo '{ARCHIVO_LOG}' para ver todos los eventos y errores.")
    # Marca en el log el fin de la simulación
    log.info("===== FIN DE LA SIMULACIÓN =====")


# Punto de entrada del programa
if __name__ == "__main__":
    main()
