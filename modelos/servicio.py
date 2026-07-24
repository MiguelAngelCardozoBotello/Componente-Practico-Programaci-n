"""
Archivo: servicio.py
Descripción: Clase abstracta Servicio del sistema integral de gestión de clientes, servicios y reservas.
"""

from abc import abstractmethod
from modelos.entidad import Entidad


class Servicio(Entidad):
    """
    Clase abstracta que representa un servicio general dentro del sistema.
    Esta clase servirá como base para los servicios especializados.
    """

    def __init__(self, identificador, nombre, costo_base, disponible=True):
        super().__init__(identificador)
        self.nombre = nombre
        self.costo_base = costo_base
        self.disponible = disponible

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, nombre):
        if not nombre or len(nombre.strip()) < 3:
            raise ValueError("El nombre del servicio debe tener mínimo 3 caracteres.")
        self._nombre = nombre.strip()

    @property
    def costo_base(self):
        return self._costo_base

    @costo_base.setter
    def costo_base(self, costo_base):
        if costo_base <= 0:
            raise ValueError("El costo base del servicio debe ser mayor que cero.")
        self._costo_base = costo_base

    @property
    def disponible(self):
        return self._disponible

    @disponible.setter
    def disponible(self, disponible):
        if not isinstance(disponible, bool):
            raise ValueError("La disponibilidad del servicio debe ser un valor booleano.")
        self._disponible = disponible

    @abstractmethod
    def calcular_costo(self):
        """
        Método abstracto que deberá calcular el costo del servicio.
        """
        pass

    @abstractmethod
    def mostrar_informacion(self):
        """
        Método abstracto que deberá mostrar la información del servicio.
        """
        pass
