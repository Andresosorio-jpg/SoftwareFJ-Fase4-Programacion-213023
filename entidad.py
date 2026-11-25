"""
entidad.py
Autor: Andrés Felipe Osorio Suarez
Copyright (c) 2026 Andrés Felipe Osorio Suarez. Todos los derechos reservados.
Clase abstracta que representa cualquier entidad general del sistema.
Curso: Programación (213023) - UNAD - Fase 4.
"""

from abc import ABC, abstractmethod  # Herramientas para definir clases abstractas
from itertools import count          # Generador de números consecutivos para los IDs


class Entidad(ABC):
    """Entidad general: todo objeto del sistema tiene un id y sabe describirse."""

    # Contador compartido por todas las entidades para generar IDs únicos
    _contador = count(1)

    def __init__(self):
        # Asigna un identificador único y privado a la entidad
        self.__id = next(Entidad._contador)

    @property
    def id(self):
        """Identificador de solo lectura (encapsulación)."""
        # Devuelve el id; no existe setter, por lo tanto no se puede modificar
        return self.__id

    @abstractmethod
    def describir(self):
        """Cada subclase debe devolver una descripción de sí misma."""
        # Método abstracto: obliga a las clases hijas a implementarlo
        raise NotImplementedError

    @abstractmethod
    def validar(self):
        """Cada subclase debe validar su propio estado."""
        # Método abstracto de validación
        raise NotImplementedError

    def __str__(self):
        # Usa el método polimórfico describir() para la representación en texto
        return self.describir()
