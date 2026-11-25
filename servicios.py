"""
servicios.py
Autor: Andrés Felipe Osorio Suarez
Copyright (c) 2026 Andrés Felipe Osorio Suarez. Todos los derechos reservados.
Clase abstracta Servicio y tres servicios especializados.
Curso: Programación (213023) - UNAD - Fase 4.

Demuestra herencia, polimorfismo (métodos sobrescritos) y sobrecarga del
cálculo de costos mediante parámetros opcionales.
"""

from abc import abstractmethod                     # Para declarar métodos abstractos
from entidad import Entidad                        # Clase abstracta base
from excepciones import (DatoInvalidoError,        # Errores propios del sistema
                         ParametroFaltanteError,
                         ServicioNoDisponibleError,
                         CalculoInconsistenteError)

# Tasa de IVA usada por defecto en Colombia
IVA = 0.19


class Servicio(Entidad):
    """Servicio genérico de Software FJ (abstracto)."""

    def __init__(self, nombre, tarifa_base, disponible=True):
        # Inicializa el id desde Entidad
        super().__init__()
        # El nombre del servicio es obligatorio
        if not nombre:
            raise ParametroFaltanteError("nombre del servicio")
        # Guarda el nombre (atributo protegido)
        self._nombre = str(nombre).strip()
        # La tarifa debe ser numérica y positiva
        if not isinstance(tarifa_base, (int, float)) or tarifa_base <= 0:
            raise DatoInvalidoError("tarifa_base", tarifa_base, "debe ser un número mayor que 0")
        # Guarda la tarifa base
        self._tarifa_base = float(tarifa_base)
        # Indica si el servicio puede reservarse
        self._disponible = bool(disponible)

    @property
    def nombre(self):
        # Devuelve el nombre del servicio
        return self._nombre

    @property
    def disponible(self):
        # Devuelve si el servicio está disponible
        return self._disponible

    def desactivar(self):
        # Marca el servicio como no disponible
        self._disponible = False

    def verificar_disponibilidad(self):
        # Lanza un error si el servicio no está disponible
        if not self._disponible:
            raise ServicioNoDisponibleError(self._nombre)

    # ---------- Métodos abstractos (polimorfismo) ----------

    @abstractmethod
    def costo_base(self, duracion):
        """Cada servicio calcula su costo base de forma diferente."""
        raise NotImplementedError

    @abstractmethod
    def validar_parametros(self, duracion):
        """Cada servicio valida la duración según sus propias reglas."""
        raise NotImplementedError

    # ---------- Método "sobrecargado" ----------

    def calcular_costo(self, duracion, impuesto=None, descuento=None):
        """
        Cálculo de costo con variantes (sobrecarga por parámetros opcionales):
          calcular_costo(d)                 -> costo base
          calcular_costo(d, impuesto=True)  -> costo + IVA (19 %)
          calcular_costo(d, impuesto=0.05)  -> costo + impuesto indicado
          calcular_costo(d, descuento=0.1)  -> costo - 10 %
          calcular_costo(d, True, 0.1)      -> descuento y luego IVA
        """
        # Valida la duración con las reglas propias del servicio
        self.validar_parametros(duracion)
        # Calcula el costo base polimórfico
        costo = self.costo_base(duracion)
        # Aplica descuento si se indicó
        if descuento is not None:
            # El descuento debe estar entre 0 y 0.5 (máximo 50 %)
            if not isinstance(descuento, (int, float)) or not 0 <= descuento <= 0.5:
                raise DatoInvalidoError("descuento", descuento, "debe estar entre 0 y 0.5")
            # Resta el porcentaje de descuento
            costo *= (1 - descuento)
        # Aplica impuesto si se indicó
        if impuesto is not None and impuesto is not False:
            # Si es True se usa el IVA por defecto, si es número se usa ese valor
            tasa = IVA if impuesto is True else impuesto
            # La tasa debe ser válida
            if not isinstance(tasa, (int, float)) or not 0 <= tasa <= 1:
                raise DatoInvalidoError("impuesto", impuesto, "debe ser True o un número entre 0 y 1")
            # Suma el impuesto
            costo *= (1 + tasa)
        # Verificación de consistencia: un costo nunca puede ser negativo o cero
        if costo <= 0:
            raise CalculoInconsistenteError(f"Costo calculado no válido: {costo}")
        # Devuelve el costo redondeado a 2 decimales
        return round(costo, 2)

    def validar(self):
        # Valida que el servicio tenga nombre y tarifa positiva
        return bool(self._nombre) and self._tarifa_base > 0


class ReservaSala(Servicio):
    """Reserva de salas: se cobra por hora según la capacidad."""

    def __init__(self, nombre, tarifa_hora, capacidad, disponible=True):
        # Inicializa la parte común del servicio
        super().__init__(nombre, tarifa_hora, disponible)
        # La capacidad debe ser un entero entre 1 y 200 personas
        if not isinstance(capacidad, int) or not 1 <= capacidad <= 200:
            raise DatoInvalidoError("capacidad", capacidad, "entero entre 1 y 200")
        # Guarda la capacidad
        self.capacidad = capacidad

    def validar_parametros(self, duracion):
        # Las salas se reservan entre 1 y 12 horas
        if not isinstance(duracion, (int, float)) or not 1 <= duracion <= 12:
            raise DatoInvalidoError("duracion", duracion, "una sala se reserva entre 1 y 12 horas")

    def costo_base(self, duracion):
        # Salas de más de 50 personas tienen recargo del 20 %
        recargo = 1.2 if self.capacidad > 50 else 1.0
        # Costo = tarifa por hora x horas x recargo
        return self._tarifa_base * duracion * recargo

    def describir(self):
        # Descripción específica de la sala (método sobrescrito)
        return f"Sala '{self._nombre}' para {self.capacidad} personas - ${self._tarifa_base:,.0f}/hora"


class AlquilerEquipo(Servicio):
    """Alquiler de equipos: se cobra por día y por unidad."""

    def __init__(self, nombre, tarifa_dia, unidades, disponible=True):
        # Inicializa la parte común del servicio
        super().__init__(nombre, tarifa_dia, disponible)
        # Debe haber al menos una unidad para alquilar
        if not isinstance(unidades, int) or unidades < 1:
            raise DatoInvalidoError("unidades", unidades, "debe ser un entero mayor o igual a 1")
        # Guarda la cantidad de unidades
        self.unidades = unidades

    def validar_parametros(self, duracion):
        # Los equipos se alquilan por días enteros, entre 1 y 30
        if not isinstance(duracion, int) or not 1 <= duracion <= 30:
            raise DatoInvalidoError("duracion", duracion, "un equipo se alquila entre 1 y 30 días enteros")

    def costo_base(self, duracion):
        # Costo = tarifa diaria x días x unidades
        costo = self._tarifa_base * duracion * self.unidades
        # Alquileres de 7 días o más tienen 15 % de descuento automático
        if duracion >= 7:
            costo *= 0.85
        # Devuelve el costo base
        return costo

    def describir(self):
        # Descripción específica del alquiler (método sobrescrito)
        return f"Equipo '{self._nombre}' x{self.unidades} - ${self._tarifa_base:,.0f}/día"


class Asesoria(Servicio):
    """Asesoría especializada: se cobra por hora según el nivel del asesor."""

    # Multiplicador de tarifa por nivel de experiencia
    NIVELES = {"junior": 1.0, "senior": 1.5, "experto": 2.0}

    def __init__(self, nombre, tarifa_hora, nivel, disponible=True):
        # Inicializa la parte común del servicio
        super().__init__(nombre, tarifa_hora, disponible)
        # El nivel debe ser uno de los permitidos
        if nivel not in self.NIVELES:
            raise DatoInvalidoError("nivel", nivel, f"use uno de {list(self.NIVELES)}")
        # Guarda el nivel
        self.nivel = nivel

    def validar_parametros(self, duracion):
        # Las asesorías duran entre 0.5 y 8 horas
        if not isinstance(duracion, (int, float)) or not 0.5 <= duracion <= 8:
            raise DatoInvalidoError("duracion", duracion, "una asesoría dura entre 0.5 y 8 horas")

    def costo_base(self, duracion):
        # Costo = tarifa x horas x multiplicador del nivel
        return self._tarifa_base * duracion * self.NIVELES[self.nivel]

    def describir(self):
        # Descripción específica de la asesoría (método sobrescrito)
        return f"Asesoría '{self._nombre}' nivel {self.nivel} - ${self._tarifa_base:,.0f}/hora"
