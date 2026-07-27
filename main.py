"""
Proyecto: Sistema Integral de Gestión de Clientes, Servicios y Reservas
Curso: Programación - Fase 4
Descripción: Archivo principal del sistema.
"""

from modelos.cliente import Cliente
from modelos.reserva_sala import ReservaSala
from modelos.asesoria import Asesoria
from modelos.alquiler_equipo import AlquilerEquipo
from modelos.reserva import Reserva
from excepciones.excepciones_reserva import ReservaError
from utils.logger_config import obtener_logger

logger = obtener_logger(__name__)


def main():
    """
    Función principal del sistema.
    En este punto se realizan pruebas iniciales de la clase Cliente
    y de los servicios especializados del sistema.
    """

    print("Sistema Integral de Gestión de Clientes, Servicios y Reservas")
    print("Proyecto Fase 4 - Programación")
    print("Inicio de la aplicación")
    print("-" * 60)

    try:
        cliente = Cliente(
            identificador=1,
            nombre="Miguel Ángel Cardozo",
            documento="123456789",
            correo="miguel.cardozo@correo.com",
            telefono="3157749365"
        )

        print("Cliente creado correctamente:")
        print(cliente.mostrar_informacion())
        print("-" * 60)

        reserva_sala = ReservaSala(
            identificador=101,
            nombre="Reserva de sala de reuniones",
            costo_base=50000,
            capacidad=20,
            horas=3
        )

        asesoria = Asesoria(
            identificador=102,
            nombre="Asesoría especializada",
            costo_base=80000,
            especialista="Consultor en sistemas",
            horas=2
        )

        alquiler_equipo = AlquilerEquipo(
            identificador=103,
            nombre="Alquiler de equipo portátil",
            costo_base=60000,
            tipo_equipo="Computador portátil",
            dias=4
        )

        print("Servicios especializados creados correctamente:")
        print(reserva_sala.mostrar_informacion())
        print(asesoria.mostrar_informacion())
        print(alquiler_equipo.mostrar_informacion())

    except ValueError as error:
        print("Error durante la ejecución del sistema:")
        print(error)

    print("-" * 60)

    # Pruebas y simulaciones de la clase Reserva (Issue #4).
    probar_reservas()


def probar_reservas():
    """
    Ejecuta simulaciones de reservas (válidas e inválidas) sobre el sistema.
    Cada simulación se aísla en su propio try/except para que un error en
    una reserva no detenga la ejecución de las demás, cumpliendo con el
    requisito de estabilidad de la aplicación.
    """

    print("Simulaciones del módulo de Reservas (Issue #4)")
    print("-" * 60)

    # --- Datos base reutilizables ---
    cliente_1 = Cliente(1, "Laura Gómez", "1020304050", "laura@correo.com", "3001234567")
    cliente_2 = Cliente(2, "Carlos Pérez", "1122334455", "carlos@correo.com", "3109876543")

    sala = ReservaSala(1, "Sala Ejecutiva A", 50000, capacidad=10, horas=2)
    asesoria_marketing = Asesoria(2, "Asesoría en Marketing", 80000, especialista="Ana Ríos", horas=3)
    equipo = AlquilerEquipo(3, "Videobeam", 30000, tipo_equipo="Proyector", dias=1)
    equipo_no_disponible = AlquilerEquipo(4, "Laptop", 40000, tipo_equipo="Portátil", dias=2, disponible=False)

    simulaciones = [
        ("Reserva válida de sala (flujo completo: confirmar y procesar)",
         lambda: _flujo_completo_valido(1, cliente_1, sala)),

        ("Reserva válida de asesoría (flujo completo)",
         lambda: _flujo_completo_valido(2, cliente_2, asesoria_marketing)),

        ("Reserva válida de alquiler de equipo (flujo completo)",
         lambda: _flujo_completo_valido(3, cliente_1, equipo)),

        ("Reserva con cliente inválido",
         lambda: Reserva(4, "no-es-un-cliente", sala, "2026-08-01", 2)),

        ("Reserva con servicio inválido",
         lambda: Reserva(5, cliente_1, "no-es-un-servicio", "2026-08-01", 2)),

        ("Reserva sobre un servicio no disponible",
         lambda: Reserva(6, cliente_2, equipo_no_disponible, "2026-08-01", 1)),

        ("Reserva con fecha en formato inválido",
         lambda: Reserva(7, cliente_1, sala, "01/08/2026", 2)),

        ("Reserva con duración negativa",
         lambda: Reserva(8, cliente_1, sala, "2026-08-01", -3)),

        ("Intentar procesar una reserva sin confirmarla antes",
         lambda: _procesar_sin_confirmar(9, cliente_2, asesoria_marketing)),

        ("Intentar cancelar una reserva que ya fue procesada",
         lambda: _cancelar_ya_procesada(10, cliente_1, equipo)),

        ("Calcular costo con un descuento inválido (mayor al 100%)",
         lambda: _descuento_invalido(11, cliente_2, sala)),

        ("Intentar confirmar una reserva dos veces",
         lambda: _confirmar_dos_veces(12, cliente_1, sala)), 
    ]

    for numero, (descripcion, accion) in enumerate(simulaciones, start=1):
        print(f"--- Simulación {numero}: {descripcion} ---")
        try:
            resultado = accion()
            if resultado is not None:
                print(resultado)
        except ReservaError as e:
            # Excepciones propias del dominio de reservas: se registran
            # en el log y la aplicación continúa sin detenerse.
            print(f"[ERROR CONTROLADO] {e}")
        except Exception as e:
            # Red de seguridad final ante cualquier error no previsto.
            logger.error(f"Error inesperado en la simulación '{descripcion}': {e}")
            print(f"[ERROR INESPERADO] {e}")
        print()

    print("Fin de las simulaciones de Reserva")
    print("-" * 60)


def _flujo_completo_valido(identificador, cliente, servicio):
    reserva = Reserva(identificador, cliente, servicio, "2026-08-01", 2)
    reserva.confirmar()
    reserva.procesar()
    return reserva.mostrar_informacion()


def _procesar_sin_confirmar(identificador, cliente, servicio):
    reserva = Reserva(identificador, cliente, servicio, "2026-08-05", 1)
    reserva.procesar()  # Debe fallar: aún está "pendiente".
    return reserva.mostrar_informacion()


def _cancelar_ya_procesada(identificador, cliente, servicio):
    reserva = Reserva(identificador, cliente, servicio, "2026-08-06", 1)
    reserva.confirmar()
    reserva.procesar()
    reserva.cancelar()  # Debe fallar: ya está "procesada".
    return reserva.mostrar_informacion()


def _descuento_invalido(identificador, cliente, servicio):
    reserva = Reserva(identificador, cliente, servicio, "2026-08-07", 1)
    reserva.calcular_costo_total(descuento=150)  # Debe fallar: > 100%.
    return reserva.mostrar_informacion()


if __name__ == "__main__":
    main()