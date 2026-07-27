"""
Archivo: reserva.py
Descripción: Clase Reserva del sistema integral de gestión de clientes,
servicios y reservas. Issue #4 - Implementar reservas.

Integra un Cliente con un Servicio, gestiona el ciclo de vida de la reserva
(pendiente -> confirmada -> procesada, o cancelada en cualquier punto previo
a ser procesada) y calcula su costo total, aplicando manejo robusto de
excepciones (personalizadas, try/except/else/finally y encadenamiento) y
registro de eventos en logs/sistema.log.
"""

from datetime import datetime

from modelos.entidad import Entidad
from modelos.cliente import Cliente
from modelos.servicio import Servicio
from excepciones.excepciones_reserva import (
    ClienteInvalidoError,
    ServicioInvalidoError,
    ServicioNoDisponibleError,
    DuracionInvalidaError,
    FechaInvalidaError,
    EstadoReservaError,
    CostoInvalidoError,
    ReservaError,
    ReservaDuplicadaError,
    LogError,
)
from utils.logger_config import obtener_logger

logger = obtener_logger(__name__)


class Reserva(Entidad):
    """
    Clase que representa una reserva dentro del sistema.
    Hereda de la clase abstracta Entidad, igual que Cliente y Servicio,
    manteniendo la coherencia del diseño orientado a objetos del proyecto.
    """

    ESTADOS_VALIDOS = ("pendiente", "confirmada", "cancelada", "procesada")
    FORMATO_FECHA = "%Y-%m-%d"

    def __init__(self, identificador, cliente, servicio, fecha, duracion):
        super().__init__(identificador)
        self.cliente = cliente
        self.servicio = servicio
        self.fecha = fecha
        self.duracion = duracion
        self._estado = "pendiente"
        self._costo_total = None
        logger.info(
            f"Reserva {self.identificador} creada en estado 'pendiente' "
            f"para el cliente {self.cliente.nombre} y el servicio {self.servicio.nombre}."
        )

    # ---------------------------------------------------------------
    # Propiedades con validación (encapsulación)
    # ---------------------------------------------------------------

    @property
    def cliente(self):
        return self._cliente

    @cliente.setter
    def cliente(self, cliente):
        if not isinstance(cliente, Cliente):
            error = ClienteInvalidoError(
                "El cliente asociado a la reserva no es una instancia válida de Cliente."
            )
            logger.error(str(error))
            raise error
        self._cliente = cliente

    @property
    def servicio(self):
        return self._servicio

    @servicio.setter
    def servicio(self, servicio):
        if not isinstance(servicio, Servicio):
            error = ServicioInvalidoError(
                "El servicio asociado a la reserva no es una instancia válida de Servicio."
            )
            logger.error(str(error))
            raise error
        if not servicio.disponible:
            error = ServicioNoDisponibleError(
                f"El servicio '{servicio.nombre}' no se encuentra disponible actualmente."
            )
            logger.error(str(error))
            raise error
        self._servicio = servicio

    @property
    def fecha(self):
        return self._fecha

    @fecha.setter
    def fecha(self, fecha):
        try:
            datetime.strptime(fecha, self.FORMATO_FECHA)
        except (TypeError, ValueError) as e:
            error = FechaInvalidaError(
                f"La fecha '{fecha}' no tiene un formato válido (se espera AAAA-MM-DD)."
            )
            logger.error(str(error))
            raise error from e
        self._fecha = fecha

    @property
    def duracion(self):
        return self._duracion

    @duracion.setter
    def duracion(self, duracion):
        # Validación estricta: ni negativos, ni cero, ni tipos incorrectos.
        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)) or duracion <= 0:
            error = DuracionInvalidaError(
                "La duración de la reserva debe ser un número mayor que cero."
            )
            logger.error(str(error))
            raise error
        self._duracion = duracion

    @property
    def estado(self):
        return self._estado

    @property
    def costo_total(self):
        return self._costo_total

    # ---------------------------------------------------------------
    # Cálculo de costo
    # ---------------------------------------------------------------

    def calcular_costo_total(self, descuento=0, incluir_impuestos=True):
        """
        Calcula el costo total de la reserva a partir del costo del servicio
        asociado y la duración de la reserva.

        Parámetros:
            descuento (float): porcentaje de descuento a aplicar (0-100).
            incluir_impuestos (bool): si se debe aplicar el IVA (19%).

        Nota de diseño: se mantiene siempre esta misma firma (sin variantes
        con distinta cantidad de parámetros), para que el cálculo de costos
        sea consistente y no dependa de capturar TypeError para "adivinar"
        qué parámetros aceptar cada implementación.

        Se valida explícitamente que el descuento esté entre 0 y 100, y que
        el costo final nunca pueda quedar en negativo, evitando el problema
        detectado en una entrega anterior donde la suma de varios descuentos
        podía superar el 100% y producir precios negativos.
        """
        if isinstance(descuento, bool) or not isinstance(descuento, (int, float)) or not (0 <= descuento <= 100):
            error = CostoInvalidoError("El descuento debe ser un porcentaje entre 0 y 100.")
            logger.error(str(error))
            raise error

        try:
            costo_base = self.servicio.calcular_costo() * self.duracion
        except (AttributeError, TypeError) as e:
            error = CostoInvalidoError(
                f"No fue posible calcular el costo base del servicio para la reserva {self.identificador}."
            )
            logger.error(str(error))
            raise error from e

        if costo_base <= 0:
            error = CostoInvalidoError("El costo base calculado debe ser mayor que cero.")
            logger.error(str(error))
            raise error

        costo_con_descuento = costo_base * (1 - descuento / 100)
        costo_final = costo_con_descuento * 1.19 if incluir_impuestos else costo_con_descuento

        # Guardia adicional: nunca debe llegar un costo negativo al cliente.
        if costo_final < 0:
            error = CostoInvalidoError("El costo final de la reserva no puede ser negativo.")
            logger.error(str(error))
            raise error

        self._costo_total = round(costo_final, 2)
        return self._costo_total

    # ---------------------------------------------------------------
    # Gestión del ciclo de vida de la reserva
    # ---------------------------------------------------------------

    def confirmar(self):
        """
        Confirma la reserva, calculando previamente su costo total.
        Demuestra try/except/else/finally y encadenamiento de excepciones.
        """
        if self.estado != "pendiente":
            error = EstadoReservaError(
                f"No se puede confirmar la reserva {self.identificador} "
                f"porque su estado actual es '{self.estado}'."
            )
            logger.error(str(error))
            raise error

        try:
            costo = self.calcular_costo_total()
        except CostoInvalidoError as e:
            logger.error(f"Fallo al confirmar la reserva {self.identificador}: {e}")
            raise ReservaError(
                f"No fue posible confirmar la reserva {self.identificador} "
                f"debido a un error en el cálculo del costo."
            ) from e
        else:
            self._estado = "confirmada"
            logger.info(f"Reserva {self.identificador} confirmada. Costo total: ${costo}")
        finally:
            logger.debug(f"Intento de confirmación finalizado para la reserva {self.identificador}.")

    def cancelar(self):
        """
        Cancela la reserva, siempre que no haya sido previamente procesada.
        """
        if self.estado == "cancelada":
            error = EstadoReservaError(f"La reserva {self.identificador} ya se encuentra cancelada.")
            logger.error(str(error))
            raise error
        if self.estado == "procesada":
            error = EstadoReservaError(
                f"No se puede cancelar la reserva {self.identificador} porque ya fue procesada."
            )
            logger.error(str(error))
            raise error

        self._estado = "cancelada"
        logger.info(f"Reserva {self.identificador} cancelada.")

    def procesar(self):
        """
        Procesa una reserva previamente confirmada. Si el servicio dejó de
        estar disponible entre la confirmación y el procesamiento, la reserva
        se cancela automáticamente y se encadena la excepción original.
        """
        if self.estado != "confirmada":
            error = EstadoReservaError(
                f"La reserva {self.identificador} debe estar confirmada antes de "
                f"procesarse (estado actual: '{self.estado}')."
            )
            logger.error(str(error))
            raise error

        try:
            if not self.servicio.disponible:
                raise ServicioNoDisponibleError(
                    f"El servicio '{self.servicio.nombre}' dejó de estar disponible."
                )
        except ServicioNoDisponibleError as e:
            logger.error(str(e))
            self._estado = "cancelada"
            raise ReservaError(
                f"La reserva {self.identificador} no pudo procesarse y fue cancelada automáticamente."
            ) from e
        else:
            self._estado = "procesada"
            logger.info(f"Reserva {self.identificador} procesada exitosamente.")
        finally:
            logger.debug(f"Intento de procesamiento finalizado para la reserva {self.identificador}.")

    # ---------------------------------------------------------------
    # Representación
    # ---------------------------------------------------------------

    def mostrar_informacion(self):
        """
        Muestra la información completa de la reserva.
        """
        costo = f"${self.costo_total}" if self.costo_total is not None else "No calculado"
        return (
            f"Reserva #{self.identificador} | "
            f"Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | "
            f"Fecha: {self.fecha} | "
            f"Duración: {self.duracion} | "
            f"Estado: {self.estado} | "
            f"Costo total: {costo}"
        )