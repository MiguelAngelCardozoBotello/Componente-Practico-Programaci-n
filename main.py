"""
Proyecto: Sistema Integral de Gestión de Clientes, Servicios y Reservas
Curso: Programación - Fase 4
Descripción: Archivo principal del sistema.
"""
from modelos.cliente import Cliente
def main():
    """
    Función principal del sistema.
    En este punto se realiza una prueba inicial de la clase Cliente.
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

    except ValueError as error:
        print("Error al crear el cliente:")
        print(error)


if __name__ == "__main__":
    main()
