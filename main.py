"""
main.py
Simulación de Software FJ: 12 operaciones completas (válidas e inválidas).

Cada operación se ejecuta dentro de su propio bloque try/except, de modo que
un error grave nunca detiene el programa: se registra en el log y se continúa.
"""

from entidades import Cliente
from excepciones import ErrorSoftwareFJ
from logger_config import RUTA_LOG, log
from reservas import Reserva
from servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala

# Listas internas (sustituyen a una base de datos)
clientes = []
servicios = []
reservas = []


def ejecutar(numero, titulo, accion):
    """
    Ejecuta una operación de la simulación capturando cualquier error del
    sistema. Devuelve el resultado de la acción o None si hubo error.
    """
    print(f"\n--- Operación {numero}: {titulo}")
    log.info(f"=== Operación {numero}: {titulo}")
    try:
        resultado = accion()
    except ErrorSoftwareFJ as error:
        # Error controlado del sistema: se muestra y se registra
        print(f"   ERROR CONTROLADO -> {error}")
        log.error(f"Operación {numero} falló: {error}")
        # Si el error tiene una causa encadenada, también se registra
        if error.__cause__ is not None:
            print(f"   Causa original   -> {error.__cause__}")
            log.error(f"   Causa original: {error.__cause__}")
        return None
    except Exception as error:  # Error inesperado: tampoco detiene el programa
        print(f"   ERROR INESPERADO -> {type(error).__name__}: {error}")
        log.critical(f"Operación {numero} error inesperado: "
                     f"{type(error).__name__}: {error}")
        return None
    else:
        print("   OK ->", resultado)
        return resultado
    finally:
        # Siempre se deja constancia del cierre de la operación
        log.debug(f"Cierre de la operación {numero}.")


def main():
    log.info("##### INICIO DE LA SIMULACIÓN DE SOFTWARE FJ #####")
    print("=" * 62)
    print("  SOFTWARE FJ - Gestión de Clientes, Servicios y Reservas")
    print("=" * 62)

    # ---------- Clientes ----------
    # 1. Cliente válido
    c1 = ejecutar(1, "Registrar cliente válido (Ana Gómez)",
                  lambda: Cliente("C001", "ana gómez", "ana.gomez@correo.com", "3101234567"))
    if c1:
        clientes.append(c1)

    # 2. Cliente con correo inválido
    c2 = ejecutar(2, "Registrar cliente con correo inválido",
                  lambda: Cliente("C002", "Luis Pérez", "luis.perez#correo", "3207654321"))
    if c2:
        clientes.append(c2)

    # 3. Cliente con parámetro faltante (nombre vacío)
    c3 = ejecutar(3, "Registrar cliente sin nombre (parámetro faltante)",
                  lambda: Cliente("C003", "", "maria@correo.com", "3001112233"))
    if c3:
        clientes.append(c3)

    # 4. Segundo cliente válido
    c4 = ejecutar(4, "Registrar cliente válido (Carlos Ruiz)",
                  lambda: Cliente("C004", "Carlos Ruiz", "carlos.ruiz@correo.com", "3159876543"))
    if c4:
        clientes.append(c4)

    # ---------- Servicios ----------
    # 5. Sala válida
    s1 = ejecutar(5, "Crear servicio: sala de reuniones válida",
                  lambda: ReservaSala("S001", "Sala Ejecutiva", 50000, 10))
    if s1:
        servicios.append(s1)

    # 6. Equipo con tarifa inválida
    s2 = ejecutar(6, "Crear equipo con tarifa negativa",
                  lambda: AlquilerEquipo("S002", "Portátil Gamer", -15000, "Portátil"))
    if s2:
        servicios.append(s2)

    # 7. Asesoría válida
    s3 = ejecutar(7, "Crear servicio: asesoría especializada válida",
                  lambda: AsesoriaEspecializada("S003", "Asesoría en Python", 80000, "senior"))
    if s3:
        servicios.append(s3)

    # Equipo válido y un servicio marcado como no disponible (para pruebas)
    s4 = AlquilerEquipo("S004", "Proyector Full HD", 12000, "Proyector")
    servicios.append(s4)
    s5 = ReservaSala("S005", "Sala de Capacitación", 40000, 25, disponible=False)
    servicios.append(s5)

    # ---------- Reservas ----------
    # 8. Reserva exitosa: crear, confirmar y procesar con IVA y descuento
    def reserva_exitosa():
        r = Reserva("R001", c1, s1, 3)
        reservas.append(r)
        r.confirmar()
        r.procesar(impuesto=0.19, descuento=0.10)
        return r.describir()
    ejecutar(8, "Reserva exitosa (sala 3 h, IVA 19 % y descuento 10 %)", reserva_exitosa)

    # 9. Reserva sobre servicio no disponible
    ejecutar(9, "Reserva de servicio no disponible",
             lambda: Reserva("R002", c4, s5, 2))

    # 10. Reserva con duración inválida (error encadenado)
    ejecutar(10, "Reserva con duración inválida (12 h en una asesoría)",
             lambda: Reserva("R003", c4, s3, 12))

    # 11. Procesar una reserva sin confirmarla (operación no permitida)
    def procesar_sin_confirmar():
        r = Reserva("R004", c4, s4, 5)
        reservas.append(r)
        return r.procesar()
    ejecutar(11, "Procesar reserva sin confirmar", procesar_sin_confirmar)

    # 12. Cálculo inconsistente (descuento fuera de rango, error encadenado)
    def calculo_inconsistente():
        r = Reserva("R005", c1, s3, 2)
        reservas.append(r)
        r.confirmar()
        return r.procesar(impuesto=0.19, descuento=0.90)
    ejecutar(12, "Cálculo inconsistente (descuento del 90 %)", calculo_inconsistente)

    # 13. Cancelar una reserva dos veces (segunda vez falla)
    def cancelar_dos_veces():
        r = Reserva("R006", c4, s4, 4)
        reservas.append(r)
        r.cancelar()
        r.cancelar()
    ejecutar(13, "Cancelar la misma reserva dos veces", cancelar_dos_veces)

    # ---------- Resumen ----------
    print("\n" + "=" * 62)
    print("  RESUMEN FINAL (el programa siguió funcionando ante los errores)")
    print("=" * 62)
    print(f"Clientes registrados : {len(clientes)}")
    for c in clientes:
        print("  -", c.describir())
    print(f"Servicios creados    : {len(servicios)}")
    for s in servicios:
        print("  -", s.describir())
    print(f"Reservas creadas     : {len(reservas)}")
    for r in reservas:
        print("  -", r.describir())
    print(f"\nRegistro de eventos y errores guardado en: {RUTA_LOG}")
    log.info("##### FIN DE LA SIMULACIÓN: el sistema terminó sin interrupciones #####")


# Punto de entrada del programa
if __name__ == "__main__":
    main()
