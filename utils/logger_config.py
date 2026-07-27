"""
Archivo: logger_config.py
Descripción: Configuración centralizada del sistema de logging. Todos los
módulos del proyecto (Cliente, Servicio, Reserva, main.py) pueden usar
obtener_logger(__name__) para registrar eventos y errores en logs/sistema.log,
cumpliendo el requisito de "todos los errores se registran correctamente".
"""

import logging
import os

_LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
os.makedirs(_LOG_DIR, exist_ok=True)
_LOG_FILE = os.path.join(_LOG_DIR, "sistema.log")


def obtener_logger(nombre):
    """
    Devuelve un logger configurado que escribe en logs/sistema.log y también
    imprime en consola. Evita duplicar handlers si el logger ya existe.
    """
    logger = logging.getLogger(nombre)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        formato = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        )

        manejador_archivo = logging.FileHandler(_LOG_FILE, encoding="utf-8")
        manejador_archivo.setLevel(logging.DEBUG)
        manejador_archivo.setFormatter(formato)
        logger.addHandler(manejador_archivo)

        manejador_consola = logging.StreamHandler()
        manejador_consola.setLevel(logging.INFO)
        manejador_consola.setFormatter(formato)
        logger.addHandler(manejador_consola)

    return logger

def registrar_evento(logger, nivel, mensaje):
    """
    Registra un evento en el log según el nivel indicado.
    Niveles soportados: INFO, WARNING, ERROR y DEBUG.
    """
    nivel = nivel.upper()

    if nivel == "INFO":
        logger.info(mensaje)
    elif nivel == "WARNING":
        logger.warning(mensaje)
    elif nivel == "ERROR":
        logger.error(mensaje)
    elif nivel == "DEBUG":
        logger.debug(mensaje)
    else:
        logger.info(mensaje)