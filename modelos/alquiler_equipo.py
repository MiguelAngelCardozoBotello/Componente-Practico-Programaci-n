"""
Archivo: alquiler_equipo.py
Descripción: Clase AlquilerEquipo, servicio especializado para el alquiler de equipos.
"""

from modelos.servicio import Servicio


class AlquilerEquipo(Servicio):
    """
    Clase que representa el servicio especializado de alquiler de equipos.
    Hereda de la clase abstracta Servicio y aplica polimorfismo mediante
    la implementación de los métodos calcular_costo() y mostrar_informacion().
    """

    def __init__(self, identificador, nombre, costo_base, tipo_equipo, dias, disponible=True):
        super().__init__(identificador, nombre, costo_base, disponible)
        self.tipo_equipo = tipo_equipo
        self.dias = dias

    @property
    def tipo_equipo(self):
        return self._tipo_equipo

    @tipo_equipo.setter
    def tipo_equipo(self, tipo_equipo):
        if not tipo_equipo or len(tipo_equipo.strip()) < 3:
            raise ValueError("El tipo de equipo debe tener mínimo 3 caracteres.")
        self._tipo_equipo = tipo_equipo.strip()

    @property
    def dias(self):
        return self._dias

    @dias.setter
    def dias(self, dias):
        if dias <= 0:
            raise ValueError("La cantidad de días de alquiler debe ser mayor que cero.")
        self._dias = dias

    def calcular_costo(self):
        """
        Calcula el costo total del alquiler del equipo.
        """
        return self.costo_base * self.dias

    def mostrar_informacion(self):
        """
        Muestra la información del servicio de alquiler de equipo.
        """
        return (
            f"Servicio: {self.nombre} | "
            f"Tipo de equipo: {self.tipo_equipo} | "
            f"Días de alquiler: {self.dias} | "
            f"Costo total: ${self.calcular_costo()}"
        )
