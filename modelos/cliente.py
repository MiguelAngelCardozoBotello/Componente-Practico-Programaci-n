"""
Archivo: cliente.py
Descripción: Clase Cliente del sistema integral de gestión de clientes, servicios y reservas.
"""

from modelos.entidad import Entidad


class Cliente(Entidad):
    """
    Clase que representa a un cliente dentro del sistema.
    Aplica encapsulación, validación de datos y hereda de la clase abstracta Entidad.
    """

    def __init__(self, identificador, nombre, documento, correo, telefono):
        super().__init__(identificador)
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, nombre):
        if not nombre or len(nombre.strip()) < 3:
            raise ValueError("El nombre del cliente debe tener mínimo 3 caracteres.")
        self._nombre = nombre.strip()

    @property
    def documento(self):
        return self._documento

    @documento.setter
    def documento(self, documento):
        if not documento or not documento.isdigit():
            raise ValueError("El documento del cliente debe contener solo números.")
        if len(documento) < 6:
            raise ValueError("El documento del cliente debe tener mínimo 6 dígitos.")
        self._documento = documento

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, correo):
        if not correo or "@" not in correo or "." not in correo:
            raise ValueError("El correo electrónico ingresado no es válido.")
        self._correo = correo.strip()

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, telefono):
        if not telefono or not telefono.isdigit():
            raise ValueError("El teléfono del cliente debe contener solo números.")
        if len(telefono) < 7:
            raise ValueError("El teléfono del cliente debe tener mínimo 7 dígitos.")
        self._telefono = telefono

    def mostrar_informacion(self):
        """
        Muestra la información básica del cliente.
        """
        return (
            f"Cliente: {self.nombre} | "
            f"Documento: {self.documento} | "
            f"Correo: {self.correo} | "
            f"Teléfono: {self.telefono}"
        )
