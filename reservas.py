"""
reservas.py
Clase Reserva: integra cliente, servicio, duración y estado, con
confirmación, cancelación y procesamiento con manejo de excepciones
(try/except, try/except/else, try/except/finally y encadenamiento).
"""

from entidades import Cliente, Entidad
from excepciones import (CalculoInconsistenteError, ErrorSoftwareFJ,
                         OperacionNoPermitidaError, ReservaInvalidaError,
                         ServicioNoDisponibleError)
from logger_config import log
from servicios import Servicio


class Reserva(Entidad):
    """Reserva de un servicio por parte de un cliente."""

    # Estados posibles de una reserva
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"
    PROCESADA = "PROCESADA"

    def __init__(self, identificador, cliente, servicio, duracion_horas):
        super().__init__(identificador)
        # Se verifica que los objetos sean del tipo correcto
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva requiere un Cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva requiere un Servicio válido.")
        # Un servicio no disponible no puede reservarse
        if not servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{servicio.nombre}' no está disponible.")
        # Se valida la duración con las reglas propias del servicio, y si
        # falla se encadena la causa original con 'raise ... from ...'
        try:
            servicio.validar_parametros(duracion_horas)
        except ErrorSoftwareFJ as causa:
            raise ReservaInvalidaError(
                f"No se pudo crear la reserva {identificador}: duración rechazada."
            ) from causa

        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion_horas
        self._estado = self.PENDIENTE
        self._costo_total = None
        log.info(f"Reserva {identificador} creada (PENDIENTE): "
                 f"{cliente.nombre} -> {servicio.nombre}, {duracion_horas} h.")

    @property
    def estado(self):
        return self._estado

    @property
    def costo_total(self):
        return self._costo_total

    def confirmar(self):
        """Pasa la reserva de PENDIENTE a CONFIRMADA."""
        if self._estado != self.PENDIENTE:
            raise OperacionNoPermitidaError(
                f"No se puede confirmar la reserva {self.identificador} "
                f"en estado {self._estado}.")
        self._estado = self.CONFIRMADA
        log.info(f"Reserva {self.identificador} CONFIRMADA.")

    def cancelar(self):
        """Cancela una reserva que no esté ya cancelada ni procesada."""
        if self._estado in (self.CANCELADA, self.PROCESADA):
            raise OperacionNoPermitidaError(
                f"No se puede cancelar la reserva {self.identificador} "
                f"en estado {self._estado}.")
        self._estado = self.CANCELADA
        log.warning(f"Reserva {self.identificador} CANCELADA.")

    def procesar(self, impuesto=None, descuento=0.0):
        """
        Procesa una reserva confirmada: calcula el costo y la marca PROCESADA.
        Usa try/except/else/finally y encadena excepciones.
        """
        try:
            # Solo se procesan reservas confirmadas
            if self._estado != self.CONFIRMADA:
                raise OperacionNoPermitidaError(
                    f"La reserva {self.identificador} debe estar CONFIRMADA "
                    f"para procesarse (estado actual: {self._estado}).")
            costo = self._servicio.calcular_costo(self._duracion, impuesto, descuento)
        except CalculoInconsistenteError as causa:
            # Se encadena el error de cálculo dentro de un error de reserva
            raise ReservaInvalidaError(
                f"Falló el cálculo de la reserva {self.identificador}.") from causa
        else:
            # Solo se ejecuta si NO hubo excepción en el bloque try
            self._costo_total = costo
            self._estado = self.PROCESADA
            log.info(f"Reserva {self.identificador} PROCESADA. "
                     f"Costo total: ${costo:,.2f}")
            return costo
        finally:
            # Se ejecuta SIEMPRE, haya o no error
            log.debug(f"Fin del intento de procesar la reserva {self.identificador} "
                      f"(estado: {self._estado}).")

    def describir(self):
        costo = f"${self._costo_total:,.2f}" if self._costo_total else "pendiente"
        return (f"Reserva {self.identificador} [{self._estado}] | "
                f"{self._cliente.nombre} | {self._servicio.nombre} | "
                f"{self._duracion} h | Costo: {costo}")
