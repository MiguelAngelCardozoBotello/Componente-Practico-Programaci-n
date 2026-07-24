"""
Archivo: asesoria.py
Descripción: Clase Asesoria, servicio especializado para asesorías profesionales.
"""

from modelos.servicio import Servicio


class Asesoria(Servicio):
    """
    Clase que representa el servicio especializado de asesoría.
    Hereda de la clase abstracta Servicio y aplica polimorfismo mediante
    la implementación de los métodos calcular_costo() y mostrar_informacion().
    """

    def __init__(self, identificador, nombre, costo_base, especialista, horas, disponible=True):
        super().__init__(identificador, nombre, costo_base, disponible)
        self.especialista = especialista
        self.horas = horas

    @property
    def especialista(self):
        return self._especialista

    @especialista.setter
    def especialista(self, especialista):
        if not especialista or len(especialista.strip()) < 3:
            raise ValueError("El nombre del especialista debe tener mínimo 3 caracteres.")
        self._especialista = especialista.strip()

    @property
    def horas(self):
        return self._horas

    @horas.setter
    def horas(self, horas):
        if horas <= 0:
            raise ValueError("La cantidad de horas de asesoría debe ser mayor que cero.")
        self._horas = horas

    def calcular_costo(self):
        """
        Calcula el costo total de la asesoría.
        """
        return self.costo_base * self.horas

    def mostrar_informacion(self):
        """
        Muestra la información del servicio de asesoría.
        """
        return (
            f"Servicio: {self.nombre} | "
            f"Especialista: {self.especialista} | "
            f"Horas: {self.horas} | "
            f"Costo total: ${self.calcular_costo()}"
        )
