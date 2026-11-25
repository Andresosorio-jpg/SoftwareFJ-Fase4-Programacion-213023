"""
sistema.py
Autor: Andrés Felipe Osorio Suarez
Copyright (c) 2026 Andrés Felipe Osorio Suarez. Todos los derechos reservados.
Gestor central que administra clientes, servicios y reservas en listas
internas (sin base de datos).
Curso: Programación (213023) - UNAD - Fase 4.
"""

from cliente import Cliente                       # Clase Cliente
from reserva import Reserva                       # Clase Reserva
from excepciones import ClienteError, SoftwareFJError  # Errores propios
from registro_logs import obtener_logger          # Logger del sistema

# Logger compartido
log = obtener_logger()


class SistemaSoftwareFJ:
    """Administra las listas internas del sistema."""

    def __init__(self):
        # Lista interna de clientes registrados
        self.__clientes = []
        # Lista interna de servicios ofrecidos
        self.__servicios = []
        # Lista interna de reservas creadas
        self.__reservas = []

    # ---------- Clientes ----------

    def registrar_cliente(self, nombre, documento, correo, telefono=None):
        """Crea y guarda un cliente; evita documentos duplicados."""
        # Recorre la lista para comprobar que el documento no exista
        for c in self.__clientes:
            if c.documento == str(documento).strip():
                raise ClienteError(f"Ya existe un cliente con documento {documento}")
        # Crea el cliente (puede lanzar DatoInvalidoError o ParametroFaltanteError)
        cliente = Cliente(nombre, documento, correo, telefono)
        # Lo agrega a la lista interna
        self.__clientes.append(cliente)
        # Registra el evento
        log.info(f"Cliente registrado: {cliente.describir()}")
        # Devuelve el cliente creado
        return cliente

    # ---------- Servicios ----------

    def agregar_servicio(self, clase_servicio, *args, **kwargs):
        """Crea cualquier servicio (polimorfismo) y lo guarda en la lista."""
        # Instancia la clase de servicio recibida con sus argumentos
        servicio = clase_servicio(*args, **kwargs)
        # Lo agrega a la lista interna
        self.__servicios.append(servicio)
        # Registra el evento
        log.info(f"Servicio creado: {servicio.describir()}")
        # Devuelve el servicio creado
        return servicio

    # ---------- Reservas ----------

    def crear_reserva(self, cliente, servicio, duracion):
        """Crea una reserva y la guarda en la lista."""
        # Crea la reserva (puede lanzar ReservaError encadenado)
        reserva = Reserva(cliente, servicio, duracion)
        # La agrega a la lista interna
        self.__reservas.append(reserva)
        # Registra el evento
        log.info(f"Reserva creada: {reserva.describir()}")
        # Devuelve la reserva creada
        return reserva

    # ---------- Ejecución segura ----------

    def ejecutar(self, descripcion, funcion, *args, **kwargs):
        """
        Ejecuta cualquier operación sin detener el programa.
        Registra el éxito o el error en el log y devuelve el resultado o None.
        """
        try:
            # Intenta ejecutar la operación solicitada
            resultado = funcion(*args, **kwargs)
        except SoftwareFJError as error:
            # Error controlado del sistema: se registra con su causa si existe
            causa = ""
            # Si hay excepción encadenada y su texto no está ya en el mensaje, se muestra
            if error.__cause__ and str(error.__cause__) not in str(error):
                causa = f" | causa: {type(error.__cause__).__name__}: {error.__cause__}"
            log.error(f"{descripcion} -> {error}{causa}")
            print(f"  ✗ {descripcion}: {error}{causa}")
            return None
        except Exception as error:
            # Cualquier error inesperado también se registra, sin detener la app
            log.exception(f"{descripcion} -> error inesperado: {error}")
            print(f"  ✗ {descripcion}: error inesperado ({error})")
            return None
        else:
            # Se ejecuta solo si no hubo errores
            print(f"  ✓ {descripcion}")
            return resultado

    # ---------- Reporte ----------

    def resumen(self):
        """Devuelve un texto con el estado de las listas internas."""
        # Construye las líneas del reporte
        lineas = [f"Clientes: {len(self.__clientes)}",
                  f"Servicios: {len(self.__servicios)}",
                  f"Reservas: {len(self.__reservas)}"]
        # Agrega cada reserva con su estado y costo
        for r in self.__reservas:
            costo = f"${r.costo:,.2f}" if r.costo else "-"
            lineas.append(f"  {r.describir()} | costo {costo}")
        # Une las líneas en un solo texto
        return "\n".join(lineas)
