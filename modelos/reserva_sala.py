"""
Archivo: reserva_sala.py
Descripción: Clase ReservaSala, servicio especializado para la reserva de salas.
"""

from modelos.servicio import Servicio


class ReservaSala(Servicio):
    """
    Clase que representa el servicio especializado de reserva de salas.
    Hereda de la clase abstracta Servicio y aplica polimorfismo mediante
    la implementación de los métodos calcular_costo() y mostrar_informacion().
    """

    def __init__(self, identificador, nombre, costo_base, capacidad, horas, disponible=True):
        super().__init__(identificador, nombre, costo_base, disponible)
        self.capacidad = capacidad
        self.horas = horas

    @property
    def capacidad(self):
        return self._capacidad

    @capacidad.setter
    def capacidad(self, capacidad):
        if capacidad <= 0:
            raise ValueError("La capacidad de la sala debe ser mayor que cero.")
        self._capacidad = capacidad

    @property
    def horas(self):
        return self._horas

    @horas.setter
    def horas(self, horas):
        if horas <= 0:
            raise ValueError("La cantidad de horas debe ser mayor que cero.")
        self._horas = horas

    def calcular_costo(self):
        """
        Calcula el costo total de la reserva de la sala.
        """
        return self.costo_base * self.horas

    def mostrar_informacion(self):
        """
        Muestra la información del servicio de reserva de sala.
        """
        return (
            f"Servicio: {self.nombre} | "
            f"Capacidad: {self.capacidad} personas | "
            f"Horas: {self.horas} | "
            f"Costo total: ${self.calcular_costo()}"
        )
