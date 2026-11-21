"""
entidades.py
Clase abstracta Entidad y clase Cliente con encapsulación y validaciones.
"""

import re
from abc import ABC, abstractmethod

from excepciones import ClienteInvalidoError, ParametroFaltanteError
from logger_config import log


class Entidad(ABC):
    """Clase abstracta que representa cualquier entidad general del sistema."""

    def __init__(self, identificador):
        # Se exige un identificador no vacío para toda entidad
        if identificador is None or str(identificador).strip() == "":
            raise ParametroFaltanteError("La entidad requiere un identificador.")
        # Atributo protegido: solo accesible por la clase y sus hijas
        self._identificador = str(identificador).strip()

    @property
    def identificador(self):
        """Identificador de solo lectura."""
        return self._identificador

    @abstractmethod
    def describir(self):
        """Devuelve una descripción en texto de la entidad (cada hija la define)."""

    def __str__(self):
        # Por defecto, una entidad se muestra con su descripción
        return self.describir()


class Cliente(Entidad):
    """Cliente de Software FJ con datos personales encapsulados y validados."""

    # Patrón sencillo para validar correos electrónicos
    _PATRON_CORREO = re.compile(r"^[\w\.\-+]+@[\w\-]+(\.[\w\-]+)+$")

    def __init__(self, identificador, nombre, correo, telefono):
        # Se inicializa la parte común (identificador) en la clase padre
        super().__init__(identificador)
        # Los datos personales son privados (doble guion bajo) y se validan
        # a través de los setters definidos como propiedades.
        self.__nombre = None
        self.__correo = None
        self.__telefono = None
        # Se asignan usando las propiedades para disparar las validaciones
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        log.info(f"Cliente creado correctamente: {self.identificador} - {self.nombre}")

    # ----------------------------- nombre -----------------------------
    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        # Parámetro faltante: None o cadena vacía
        if valor is None or not str(valor).strip():
            raise ParametroFaltanteError("El nombre del cliente es obligatorio.")
        # Debe ser texto con al menos 3 caracteres y solo letras/espacios
        valor = str(valor).strip()
        if len(valor) < 3 or not all(c.isalpha() or c.isspace() for c in valor):
            raise ClienteInvalidoError(
                f"Nombre inválido '{valor}': mínimo 3 letras, sin números ni símbolos.")
        self.__nombre = valor.title()

    # ----------------------------- correo -----------------------------
    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if valor is None or not str(valor).strip():
            raise ParametroFaltanteError("El correo del cliente es obligatorio.")
        valor = str(valor).strip().lower()
        if not self._PATRON_CORREO.match(valor):
            raise ClienteInvalidoError(f"Correo electrónico inválido: '{valor}'.")
        self.__correo = valor

    # ---------------------------- teléfono ----------------------------
    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        if valor is None or not str(valor).strip():
            raise ParametroFaltanteError("El teléfono del cliente es obligatorio.")
        valor = str(valor).strip()
        # Debe tener exactamente 10 dígitos (formato celular colombiano)
        if not (valor.isdigit() and len(valor) == 10):
            raise ClienteInvalidoError(
                f"Teléfono inválido '{valor}': debe tener 10 dígitos numéricos.")
        self.__telefono = valor

    def describir(self):
        """Implementación del método abstracto de Entidad."""
        return (f"Cliente {self.identificador}: {self.nombre} | "
                f"{self.correo} | Tel. {self.telefono}")
