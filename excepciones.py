"""
excepciones.py
Autor: Andrés Felipe Osorio Suarez
Copyright (c) 2026 Andrés Felipe Osorio Suarez. Todos los derechos reservados.
Excepciones personalizadas del sistema Software FJ.
Curso: Programación (213023) - UNAD - Fase 4.

Todas las excepciones del dominio heredan de SoftwareFJError, de modo que
el programa puede capturarlas de forma general o específica.
"""


class SoftwareFJError(Exception):
    """Excepción base de todo el sistema Software FJ."""

    def __init__(self, mensaje, codigo="SFJ-000"):
        # Guarda un código interno que ayuda a identificar el tipo de error en los logs
        self.codigo = codigo
        # Llama al constructor de Exception con el texto del error
        super().__init__(mensaje)

    def __str__(self):
        # Representación legible: [código] mensaje
        return f"[{self.codigo}] {super().__str__()}"


class DatoInvalidoError(SoftwareFJError):
    """Se lanza cuando un dato no cumple las reglas de validación."""

    def __init__(self, campo, valor, motivo):
        # Guarda el nombre del campo que falló
        self.campo = campo
        # Guarda el valor recibido para dejarlo en el log
        self.valor = valor
        # Construye el mensaje y lo envía a la clase base con su código
        super().__init__(f"Campo '{campo}' inválido ({valor!r}): {motivo}", "SFJ-100")


class ParametroFaltanteError(SoftwareFJError):
    """Se lanza cuando falta un parámetro obligatorio."""

    def __init__(self, parametro):
        # Guarda el nombre del parámetro ausente
        self.parametro = parametro
        # Mensaje con código propio
        super().__init__(f"Falta el parámetro obligatorio '{parametro}'", "SFJ-101")


class ClienteError(SoftwareFJError):
    """Errores relacionados con la gestión de clientes."""

    def __init__(self, mensaje):
        # Asigna el código de la familia de clientes
        super().__init__(mensaje, "SFJ-200")


class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza cuando se intenta usar un servicio inactivo o inexistente."""

    def __init__(self, nombre_servicio):
        # Guarda el servicio que se intentó usar
        self.nombre_servicio = nombre_servicio
        # Mensaje con código de servicios
        super().__init__(f"El servicio '{nombre_servicio}' no está disponible", "SFJ-300")


class CalculoInconsistenteError(SoftwareFJError):
    """Se lanza cuando un cálculo de costos produce un resultado imposible."""

    def __init__(self, mensaje):
        # Código de errores de cálculo
        super().__init__(mensaje, "SFJ-310")


class ReservaError(SoftwareFJError):
    """Errores generales de reservas (creación, confirmación, procesamiento)."""

    def __init__(self, mensaje):
        # Código de la familia de reservas
        super().__init__(mensaje, "SFJ-400")


class OperacionNoPermitidaError(ReservaError):
    """Se lanza cuando se intenta una transición de estado no válida."""

    def __init__(self, operacion, estado_actual):
        # Guarda la operación rechazada
        self.operacion = operacion
        # Guarda el estado en que estaba la reserva
        self.estado_actual = estado_actual
        # Construye el mensaje usando la clase padre ReservaError
        super().__init__(f"No se puede '{operacion}' una reserva en estado '{estado_actual}'")
        # Sobrescribe el código para distinguirla de ReservaError
        self.codigo = "SFJ-410"
