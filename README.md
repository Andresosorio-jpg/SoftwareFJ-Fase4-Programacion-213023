# Sistema Integral de Gestión de Clientes, Servicios y Reservas – Software FJ

**Autor: Andrés Felipe Osorio Suarez**

**Universidad Nacional Abierta y a Distancia – UNAD**
Escuela de Ciencias Básicas, Tecnología e Ingeniería (ECBTI) · Ingeniería de Sistemas
Curso: **Programación (213023)** · Fase 4 – Prácticas simuladas

Aplicación en Python orientada a objetos, **sin base de datos**, que gestiona clientes, servicios
(reservas de salas, alquiler de equipos y asesorías especializadas) y reservas para la empresa
Software FJ, con manejo avanzado de excepciones y un archivo de logs.

## Estructura del proyecto

| Archivo | Contenido |
|---|---|
| `excepciones.py` | Excepciones personalizadas (`SoftwareFJError` y sus derivadas) |
| `registro_logs.py` | Configuración del archivo de logs `software_fj.log` |
| `entidad.py` | Clase abstracta `Entidad` (id único, `describir()`, `validar()`) |
| `cliente.py` | Clase `Cliente` con validaciones y datos personales encapsulados |
| `servicios.py` | Clase abstracta `Servicio` y los servicios `ReservaSala`, `AlquilerEquipo` y `Asesoria` |
| `reserva.py` | Clase `Reserva` (confirmar, cancelar, procesar) |
| `sistema.py` | Gestor `SistemaSoftwareFJ` con listas internas y ejecución segura |
| `main.py` | Simulación de 11 operaciones válidas e inválidas |

## Conceptos aplicados

- **Abstracción:** `Entidad` y `Servicio` son clases abstractas (`abc.ABC`).
- **Herencia:** `Cliente`, `Servicio` y `Reserva` heredan de `Entidad`; los tres servicios heredan de `Servicio`.
- **Polimorfismo:** cada servicio sobrescribe `costo_base()`, `validar_parametros()` y `describir()`.
- **Encapsulación:** atributos privados (`__nombre`, `__documento`…) con propiedades y validación en los setters.
- **Sobrecarga de métodos:** `calcular_costo(duracion, impuesto=None, descuento=None)` admite varias variantes (solo base, con IVA, con impuesto propio, con descuento, o ambos).
- **Excepciones:** excepciones personalizadas, `try/except`, `try/except/else`, `try/except/else/finally` y encadenamiento con `raise ... from ...`.
- **Logs:** todos los eventos y errores quedan en `software_fj.log`.

## Ejecución

Requiere Python 3.8 o superior, sin librerías externas.

```bash
python main.py
```

El programa muestra en consola el resultado de cada operación (✓ éxito / ✗ error controlado),
termina con un resumen y nunca se detiene por un error.

## Autoría

**Autor:** Andrés Felipe Osorio Suarez

Entrega individual y de autoría exclusiva. El trabajo se presenta de forma individual
porque los demás integrantes del grupo no participaron en el foro ni en el repositorio
dentro del plazo de la actividad. El historial de commits de este repositorio registra
la fecha y hora de cada archivo.

© 2026 Andrés Felipe Osorio Suarez. Todos los derechos reservados. Ver [LICENSE](LICENSE).
