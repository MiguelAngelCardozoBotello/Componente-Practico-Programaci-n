"""
Archivo: entidad.py
Descripción: Clase abstracta general del sistema.
"""

from abc import ABC, abstractmethod


class Entidad(ABC):
    """
    Clase abstracta general para representar entidades del sistema.
    Esta clase servirá como base para otras clases del proyecto.
    """

    def __init__(self, identificador):
        self._identificador = identificador

    @property
    def identificador(self):
        return self._identificador

    @abstractmethod
    def mostrar_informacion(self):
        """
        Método abstracto que deberá ser implementado por las clases hijas.
        """
        pass
