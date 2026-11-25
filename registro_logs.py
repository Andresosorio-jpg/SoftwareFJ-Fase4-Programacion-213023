"""
registro_logs.py
Autor: Andrés Felipe Osorio Suarez
Copyright (c) 2026 Andrés Felipe Osorio Suarez. Todos los derechos reservados.
Configuración del archivo de logs donde se registran eventos y errores.
Curso: Programación (213023) - UNAD - Fase 4.
"""

import logging  # Módulo estándar de Python para registrar eventos

# Nombre del archivo donde se guardarán los eventos y errores
ARCHIVO_LOG = "software_fj.log"


def obtener_logger(nombre="SoftwareFJ"):
    """Devuelve un logger que escribe los eventos en el archivo de logs."""
    # Obtiene (o crea) un logger con el nombre indicado
    logger = logging.getLogger(nombre)
    # Si ya tiene manejadores configurados, se reutiliza para no duplicar líneas
    if logger.handlers:
        return logger
    # Nivel mínimo de mensajes que se registrarán
    logger.setLevel(logging.INFO)
    # Formato: fecha | nivel | mensaje
    formato = logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s",
                                "%Y-%m-%d %H:%M:%S")
    # Manejador que escribe en el archivo de logs (modo añadir, UTF-8)
    manejador_archivo = logging.FileHandler(ARCHIVO_LOG, mode="a", encoding="utf-8")
    # Aplica el formato al manejador de archivo
    manejador_archivo.setFormatter(formato)
    # Agrega el manejador al logger
    logger.addHandler(manejador_archivo)
    # Devuelve el logger listo para usar
    return logger
