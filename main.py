"""
Proyecto: Sistema Integral de Gestión de Clientes, Servicios y Reservas
Curso: Programación - Fase 4
Descripción: Archivo principal del sistema.
"""

from modelos.cliente import Cliente
from modelos.reserva_sala import ReservaSala
from modelos.asesoria import Asesoria
from modelos.alquiler_equipo import AlquilerEquipo


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


if __name__ == "__main__":
    main()
