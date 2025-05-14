import logging
from pathlib import Path

def init_logger(ruta_log="..logs.log", nivel=logging.INFO):
    # Crear el logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Evitar agregar múltiples handlers
    if not logger.hasHandlers():

        # Crear un handler para el archivo de log
        file_handler = logging.FileHandler(ruta_log, encoding="utf-8")
        file_handler.setLevel(nivel)  # Nivel detallado para el archivo

        # Crear un handler para la consola
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Formateador de logs
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(name)s] [%(levelname)s] -> %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Agregar handlers al logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger