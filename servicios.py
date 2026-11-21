"""
servicios.py
Clase abstracta Servicio y tres servicios especializados:
ReservaSala, AlquilerEquipo y AsesoriaEspecializada.

Se aplica polimorfismo (cada hijo sobrescribe calcular_costo, describir y
validar_parametros) y sobrecarga simulada con parámetros opcionales.
"""

from abc import abstractmethod

from entidades import Entidad
from excepciones import (CalculoInconsistenteError, ParametroFaltanteError,
                         ServicioInvalidoError)
from logger_config import log


class Servicio(Entidad):
    """Clase abstracta que modela un servicio ofrecido por Software FJ."""

    # IVA por defecto de Colombia (19 %)
    IVA_DEFECTO = 0.19

    def __init__(self, identificador, nombre, tarifa_hora, disponible=True):
        super().__init__(identificador)
        # Validaciones comunes a todos los servicios
        if nombre is None or not str(nombre).strip():
            raise ParametroFaltanteError("El nombre del servicio es obligatorio.")
        if not isinstance(tarifa_hora, (int, float)) or isinstance(tarifa_hora, bool):
            raise ServicioInvalidoError("La tarifa por hora debe ser numérica.")
        if tarifa_hora <= 0:
            raise ServicioInvalidoError("La tarifa por hora debe ser mayor que cero.")
        self._nombre = str(nombre).strip()
        self._tarifa_hora = float(tarifa_hora)
        self._disponible = bool(disponible)

    # --------- propiedades (encapsulación) ---------
    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa_hora(self):
        return self._tarifa_hora

    @property
    def disponible(self):
        return self._disponible

    @disponible.setter
    def disponible(self, valor):
        # Cambiar la disponibilidad se registra como evento relevante
        self._disponible = bool(valor)
        log.info(f"Servicio {self.identificador} marcado como "
                 f"{'disponible' if self._disponible else 'NO disponible'}.")

    # --------- métodos abstractos (obligatorios en las hijas) ---------
    @abstractmethod
    def validar_parametros(self, duracion_horas):
        """Valida la duración y los parámetros propios del servicio."""

    @abstractmethod
    def _costo_base(self, duracion_horas):
        """Costo sin impuestos ni descuentos; cada servicio lo calcula distinto."""

    # --------- método sobrecargado (simulado con parámetros opcionales) ---------
    def calcular_costo(self, duracion_horas, impuesto=None, descuento=0.0):
        """
        Calcula el costo total. Variantes de uso (sobrecarga simulada):
          calcular_costo(2)                      -> costo base
          calcular_costo(2, impuesto=0.19)       -> costo base + impuesto
          calcular_costo(2, 0.19, descuento=0.1) -> con impuesto y descuento
        """
        # Se valida primero (cada hija define sus reglas)
        self.validar_parametros(duracion_horas)
        base = self._costo_base(duracion_horas)

        # Validaciones de los parámetros opcionales
        if impuesto is not None and not (0 <= impuesto <= 1):
            raise CalculoInconsistenteError(
                f"Impuesto fuera de rango (0 a 1): {impuesto}")
        if not (0 <= descuento <= 0.5):
            raise CalculoInconsistenteError(
                f"Descuento fuera de rango (0 a 0.5): {descuento}")

        total = base
        # Se aplica el descuento sobre el valor base
        total -= base * descuento
        # Se aplica el impuesto sobre el valor ya descontado
        if impuesto is not None:
            total += total * impuesto

        # Verificación de consistencia del resultado
        if total <= 0:
            raise CalculoInconsistenteError(
                f"El costo calculado no es válido: {total}")
        return round(total, 2)

    def describir(self):
        estado = "Disponible" if self.disponible else "No disponible"
        return (f"Servicio {self.identificador}: {self.nombre} | "
                f"${self.tarifa_hora:,.0f}/hora | {estado}")


class ReservaSala(Servicio):
    """Reserva de salas de reuniones, con capacidad máxima de personas."""

    def __init__(self, identificador, nombre, tarifa_hora, capacidad, disponible=True):
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ServicioInvalidoError("La capacidad de la sala debe ser un entero positivo.")
        self._capacidad = capacidad
        log.info(f"Servicio creado: sala '{self.nombre}' (capacidad {capacidad}).")

    def validar_parametros(self, duracion_horas):
        # Una sala se reserva entre 1 y 8 horas
        if not isinstance(duracion_horas, (int, float)) or not (1 <= duracion_horas <= 8):
            raise ServicioInvalidoError(
                f"Duración inválida para sala: {duracion_horas} (permitido 1 a 8 horas).")

    def _costo_base(self, duracion_horas):
        # Costo = tarifa por hora x horas
        return self.tarifa_hora * duracion_horas

    def describir(self):
        return super().describir() + f" | Sala para {self._capacidad} personas"


class AlquilerEquipo(Servicio):
    """Alquiler de equipos (portátiles, proyectores...), con depósito fijo."""

    DEPOSITO = 20000.0

    def __init__(self, identificador, nombre, tarifa_hora, tipo_equipo, disponible=True):
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        if not tipo_equipo or not str(tipo_equipo).strip():
            raise ParametroFaltanteError("El tipo de equipo es obligatorio.")
        self._tipo_equipo = str(tipo_equipo).strip()
        log.info(f"Servicio creado: alquiler de equipo '{self._tipo_equipo}'.")

    def validar_parametros(self, duracion_horas):
        # Un equipo se alquila entre 1 y 72 horas
        if not isinstance(duracion_horas, (int, float)) or not (1 <= duracion_horas <= 72):
            raise ServicioInvalidoError(
                f"Duración inválida para equipo: {duracion_horas} (permitido 1 a 72 horas).")

    def _costo_base(self, duracion_horas):
        # Costo = tarifa x horas + depósito fijo
        return self.tarifa_hora * duracion_horas + self.DEPOSITO

    def describir(self):
        return super().describir() + f" | Equipo: {self._tipo_equipo} (+depósito)"


class AsesoriaEspecializada(Servicio):
    """Asesoría con un especialista; el costo varía según el nivel."""

    # Recargo por nivel del asesor
    RECARGOS = {"junior": 1.0, "senior": 1.5, "experto": 2.0}

    def __init__(self, identificador, nombre, tarifa_hora, nivel, disponible=True):
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        nivel = str(nivel).strip().lower() if nivel is not None else ""
        if nivel not in self.RECARGOS:
            raise ServicioInvalidoError(
                f"Nivel de asesor inválido '{nivel}': use junior, senior o experto.")
        self._nivel = nivel
        log.info(f"Servicio creado: asesoría '{self.nombre}' nivel {nivel}.")

    def validar_parametros(self, duracion_horas):
        # Una asesoría dura entre 1 y 6 horas
        if not isinstance(duracion_horas, (int, float)) or not (1 <= duracion_horas <= 6):
            raise ServicioInvalidoError(
                f"Duración inválida para asesoría: {duracion_horas} (permitido 1 a 6 horas).")

    def _costo_base(self, duracion_horas):
        # Costo = tarifa x horas x recargo del nivel
        return self.tarifa_hora * duracion_horas * self.RECARGOS[self._nivel]

    def describir(self):
        return super().describir() + f" | Asesor nivel {self._nivel}"
