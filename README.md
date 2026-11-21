# Software FJ - Sistema Integral de Gestión de Clientes, Servicios y Reservas

Proyecto del curso **Programación (213023)** - UNAD, Fase 4: manejo de excepciones en programación orientada a objetos.

Sistema en Python, sin base de datos, que gestiona clientes, servicios (salas, equipos y asesorías) y reservas, y que sigue funcionando aunque ocurran errores. Los errores y eventos se guardan en `eventos.log`.

## Requisitos
- Python 3.8 o superior (solo usa la biblioteca estándar).

## Ejecución
```bash
python main.py
```
Se simulan 13 operaciones (válidas e inválidas) y se genera el archivo `eventos.log`.

## Estructura
| Archivo | Contenido |
|---|---|
| `excepciones.py` | Excepciones personalizadas (base `ErrorSoftwareFJ` y derivadas) |
| `logger_config.py` | Configuración del archivo de logs |
| `entidades.py` | Clase abstracta `Entidad` y clase `Cliente` |
| `servicios.py` | Clase abstracta `Servicio`, `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada` |
| `reservas.py` | Clase `Reserva` (confirmar, cancelar, procesar) |
| `main.py` | Simulación de las operaciones |

## Conceptos aplicados
Abstracción, herencia, polimorfismo, encapsulación (atributos privados y `@property`), sobrecarga simulada con parámetros opcionales, excepciones personalizadas, `try/except`, `try/except/else`, `try/except/finally` y encadenamiento con `raise ... from ...`.
