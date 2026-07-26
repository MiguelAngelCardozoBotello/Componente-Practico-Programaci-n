"""
Archivo: excepciones_reserva.py
Descripción: Excepciones personalizadas para el módulo de gestión de reservas.
Todas heredan de ReservaError para poder capturarse de forma general o
específica según se necesite.
"""


class ReservaError(Exception):
    """Excepción base para cualquier error relacionado con la gestión de reservas."""
    pass


class ClienteInvalidoError(ReservaError):
    """Se lanza cuando el cliente asociado a la reserva no es válido."""
    pass


class ServicioInvalidoError(ReservaError):
    """Se lanza cuando el servicio asociado a la reserva no es una instancia válida."""
    pass


class ServicioNoDisponibleError(ReservaError):
    """Se lanza cuando se intenta reservar (o procesar) un servicio no disponible."""
    pass


class DuracionInvalidaError(ReservaError):
    """Se lanza cuando la duración de la reserva es nula, negativa o de tipo incorrecto."""
    pass


class FechaInvalidaError(ReservaError):
    """Se lanza cuando la fecha de la reserva no cumple el formato esperado (AAAA-MM-DD)."""
    pass


class EstadoReservaError(ReservaError):
    """Se lanza cuando se intenta una transición de estado no permitida
    (por ejemplo, procesar una reserva que no ha sido confirmada)."""
    pass


class CostoInvalidoError(ReservaError):
    """Se lanza cuando el cálculo del costo produce un valor inválido:
    descuentos fuera de rango, costos negativos o inconsistentes."""
    pass