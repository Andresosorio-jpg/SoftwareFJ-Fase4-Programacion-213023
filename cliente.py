"""
cliente.py
Autor: Andrés Felipe Osorio Suarez
Copyright (c) 2026 Andrés Felipe Osorio Suarez. Todos los derechos reservados.
Clase Cliente con validaciones robustas y datos personales encapsulados.
Curso: Programación (213023) - UNAD - Fase 4.
"""

import re                                         # Expresiones regulares para validar formatos
from entidad import Entidad                       # Clase abstracta base
from excepciones import DatoInvalidoError, ParametroFaltanteError  # Errores propios

# Patrón de correo electrónico sencillo: texto@texto.dominio
PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")


class Cliente(Entidad):
    """Cliente de Software FJ. Hereda de Entidad."""

    def __init__(self, nombre, documento, correo, telefono=None):
        # Inicializa la parte común (id único) desde la clase padre
        super().__init__()
        # Usa los setters para que todos los datos pasen por validación
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono
        # Validación final del objeto completo
        self.validar()

    # ---------- Propiedades encapsuladas ----------

    @property
    def nombre(self):
        # Devuelve el nombre almacenado en el atributo privado
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        # El nombre es obligatorio
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("nombre")
        # Quita espacios sobrantes al inicio y al final
        valor = str(valor).strip()
        # Solo se permiten letras (incluye tildes y ñ) y espacios
        if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñÜü ]{3,60}", valor):
            raise DatoInvalidoError("nombre", valor, "solo letras, entre 3 y 60 caracteres")
        # Guarda el nombre validado
        self.__nombre = valor

    @property
    def documento(self):
        # Devuelve el documento privado
        return self.__documento

    @documento.setter
    def documento(self, valor):
        # El documento es obligatorio
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("documento")
        # Convierte a texto sin espacios
        valor = str(valor).strip()
        # Debe ser numérico y tener entre 6 y 10 dígitos
        if not valor.isdigit() or not 6 <= len(valor) <= 10:
            raise DatoInvalidoError("documento", valor, "debe tener entre 6 y 10 dígitos")
        # Guarda el documento validado
        self.__documento = valor

    @property
    def correo(self):
        # Devuelve el correo privado
        return self.__correo

    @correo.setter
    def correo(self, valor):
        # El correo es obligatorio
        if not valor:
            raise ParametroFaltanteError("correo")
        # Normaliza a minúsculas y sin espacios
        valor = str(valor).strip().lower()
        # Verifica el formato con la expresión regular
        if not PATRON_CORREO.match(valor):
            raise DatoInvalidoError("correo", valor, "formato de correo no válido")
        # Guarda el correo validado
        self.__correo = valor

    @property
    def telefono(self):
        # Devuelve el teléfono (puede ser None porque es opcional)
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        # Si no se envía teléfono se guarda None (dato opcional)
        if valor is None:
            self.__telefono = None
            return
        # Convierte a texto sin espacios
        valor = str(valor).strip()
        # Debe ser un celular colombiano de 10 dígitos que inicia en 3
        if not re.fullmatch(r"3\d{9}", valor):
            raise DatoInvalidoError("telefono", valor, "debe ser un celular de 10 dígitos que inicie en 3")
        # Guarda el teléfono validado
        self.__telefono = valor

    # ---------- Métodos de Entidad ----------

    def validar(self):
        """Comprueba que el cliente quedó completo."""
        # Si algún dato obligatorio falta, se lanza error
        for campo in ("nombre", "documento", "correo"):
            if not getattr(self, campo, None):
                raise ParametroFaltanteError(campo)
        # Si todo está bien devuelve True
        return True

    def describir(self):
        # Oculta parte del documento para proteger el dato personal
        doc_oculto = "*" * (len(self.documento) - 4) + self.documento[-4:]
        # Devuelve la descripción del cliente
        return f"Cliente #{self.id}: {self.nombre} (doc {doc_oculto}, {self.correo})"
