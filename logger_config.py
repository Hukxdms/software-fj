"""
logger_config.py
Configuración del registro de eventos y errores (archivo de logs).

El enunciado exige un archivo de logs donde se registren todos los errores y
eventos relevantes. Se usa el módulo estándar logging escribiendo en
'eventos.log' (solo archivos para logs, sin ninguna base de datos).
"""

import logging
import os

# Ruta del archivo de log: junto a este módulo, sin importar desde dónde se ejecute
RUTA_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eventos.log")


def obtener_logger():
    """Devuelve el logger único del sistema, configurándolo la primera vez."""
    logger = logging.getLogger("software_fj")

    # Si ya tiene manejadores, ya fue configurado: se reutiliza
    if logger.handlers:
        return logger

    # Se registran mensajes desde nivel DEBUG hacia arriba
    logger.setLevel(logging.DEBUG)

    # Formato: fecha y hora | nivel | mensaje
    formato = logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s",
                                datefmt="%Y-%m-%d %H:%M:%S")

    # Manejador de archivo (modo 'w' para empezar un log limpio en cada ejecución)
    manejador_archivo = logging.FileHandler(RUTA_LOG, mode="w", encoding="utf-8")
    manejador_archivo.setFormatter(formato)
    logger.addHandler(manejador_archivo)

    # Evita que los mensajes se dupliquen en el logger raíz
    logger.propagate = False
    return logger


# Logger compartido que importan los demás módulos
log = obtener_logger()
