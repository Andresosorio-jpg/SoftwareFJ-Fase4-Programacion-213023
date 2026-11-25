"""
reserva.py
Autor: Andrés Felipe Osorio Suarez
Copyright (c) 2026 Andrés Felipe Osorio Suarez. Todos los derechos reservados.
Clase Reserva que integra cliente, servicio, duración y estado.
Curso: Programación (213023) - UNAD - Fase 4.
"""

from entidad import Entidad                         # Clase abstracta base
from cliente import Cliente                         # Para verificar el tipo de cliente
from servicios import Servicio                      # Para verificar el tipo de servicio
from excepciones import (ReservaError,              # Errores propios
                         OperacionNoPermitidaError,
                         ParametroFaltanteError,
                         SoftwareFJError)
from registro_logs import obtener_logger            # Logger del sistema

# Logger compartido del módulo
log = obtener_logger()


class Reserva(Entidad):
    """Reserva de un servicio por parte de un cliente."""

    # Estados posibles de una reserva
    PENDIENTE = "pendiente"
    CONFIRMADA = "confirmada"
    CANCELADA = "cancelada"
    PROCESADA = "procesada"

    def __init__(self, cliente, servicio, duracion):
        # Inicializa el id desde Entidad
        super().__init__()
        # Verifica que se haya enviado un cliente válido
        if not isinstance(cliente, Cliente):
            raise ParametroFaltanteError("cliente (objeto Cliente)")
        # Verifica que se haya enviado un servicio válido
        if not isinstance(servicio, Servicio):
            raise ParametroFaltanteError("servicio (objeto Servicio)")
        # Guarda las referencias (atributos privados)
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion
        # Toda reserva inicia en estado pendiente
        self.__estado = Reserva.PENDIENTE
        # El costo se calcula al procesar
        self.__costo = None
        # Valida la reserva al crearla
        self.validar()

    # ---------- Propiedades de solo lectura ----------

    @property
    def estado(self):
        # Devuelve el estado actual
        return self.__estado

    @property
    def costo(self):
        # Devuelve el costo calculado (None si no se ha procesado)
        return self.__costo

    @property
    def cliente(self):
        # Devuelve el cliente de la reserva
        return self.__cliente

    @property
    def servicio(self):
        # Devuelve el servicio reservado
        return self.__servicio

    # ---------- Métodos de Entidad ----------

    def validar(self):
        """Valida disponibilidad y duración; encadena el error original."""
        try:
            # El servicio debe estar disponible
            self.__servicio.verificar_disponibilidad()
            # La duración debe cumplir las reglas del servicio
            self.__servicio.validar_parametros(self.__duracion)
        except SoftwareFJError as error:
            # Encadenamiento de excepciones: se conserva la causa original
            raise ReservaError(f"No se pudo crear la reserva: {error}") from error
        # Si no hubo errores la reserva es válida
        return True

    def describir(self):
        # Descripción de la reserva con su estado
        return (f"Reserva #{self.id} | {self.__cliente.nombre} -> {self.__servicio.nombre} "
                f"| duración {self.__duracion} | estado {self.__estado}")

    # ---------- Operaciones de la reserva ----------

    def confirmar(self):
        """Pasa la reserva de pendiente a confirmada."""
        # Solo se puede confirmar una reserva pendiente
        if self.__estado != Reserva.PENDIENTE:
            raise OperacionNoPermitidaError("confirmar", self.__estado)
        # Cambia el estado
        self.__estado = Reserva.CONFIRMADA
        # Registra el evento en el log
        log.info(f"Reserva #{self.id} confirmada")

    def cancelar(self):
        """Cancela la reserva si aún no fue procesada."""
        # No se puede cancelar algo procesado o ya cancelado
        if self.__estado in (Reserva.PROCESADA, Reserva.CANCELADA):
            raise OperacionNoPermitidaError("cancelar", self.__estado)
        # Cambia el estado
        self.__estado = Reserva.CANCELADA
        # Registra el evento
        log.info(f"Reserva #{self.id} cancelada")

    def procesar(self, impuesto=True, descuento=None):
        """
        Calcula el costo final y marca la reserva como procesada.
        Usa try / except / else / finally.
        """
        # Solo se procesan reservas confirmadas
        if self.__estado != Reserva.CONFIRMADA:
            raise OperacionNoPermitidaError("procesar", self.__estado)
        try:
            # Intenta calcular el costo con la variante indicada
            costo = self.__servicio.calcular_costo(self.__duracion, impuesto, descuento)
        except SoftwareFJError as error:
            # Si el cálculo falla, se registra y se encadena el error
            log.error(f"Fallo al procesar reserva #{self.id}: {error}")
            raise ReservaError(f"Reserva #{self.id} no procesada") from error
        else:
            # Solo se ejecuta si no hubo error: guarda costo y cambia estado
            self.__costo = costo
            self.__estado = Reserva.PROCESADA
            log.info(f"Reserva #{self.id} procesada por ${costo:,.2f}")
            # Devuelve el costo final
            return costo
        finally:
            # Siempre se ejecuta, haya o no error
            log.info(f"Fin del intento de procesamiento de la reserva #{self.id}")
