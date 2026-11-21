"""
excepciones.py
Excepciones personalizadas del sistema Software FJ.

Todas heredan de ErrorSoftwareFJ, de modo que el programa principal puede
capturar cualquier error propio del sistema con un solo bloque except.
"""


class ErrorSoftwareFJ(Exception):
    """Excepción base de todo el sistema Software FJ."""

    def __init__(self, mensaje, codigo="FJ-000"):
        # Se llama al constructor de Exception con el mensaje legible
        super().__init__(mensaje)
        # Se guarda un código de error para facilitar el rastreo en el log
        self.codigo = codigo

    def __str__(self):
        # Formato uniforme: [CODIGO] mensaje
        return f"[{self.codigo}] {super().__str__()}"


class ClienteInvalidoError(ErrorSoftwareFJ):
    """Se lanza cuando los datos de un cliente no cumplen las validaciones."""

    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="FJ-100")


class ServicioInvalidoError(ErrorSoftwareFJ):
    """Se lanza cuando los parámetros de un servicio son inválidos."""

    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="FJ-200")


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """Se lanza cuando se intenta usar un servicio que no está disponible."""

    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="FJ-201")


class ParametroFaltanteError(ErrorSoftwareFJ):
    """Se lanza cuando falta un parámetro obligatorio en una operación."""

    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="FJ-300")


class ReservaInvalidaError(ErrorSoftwareFJ):
    """Se lanza ante intentos de reserva incorrectos (datos o estado)."""

    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="FJ-400")


class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """Se lanza cuando se pide una operación no permitida en el estado actual."""

    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="FJ-401")


class CalculoInconsistenteError(ErrorSoftwareFJ):
    """Se lanza cuando un cálculo de costos produce valores inconsistentes."""

    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="FJ-500")
