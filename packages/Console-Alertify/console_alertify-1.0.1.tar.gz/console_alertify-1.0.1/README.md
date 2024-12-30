# Console-Alertify - Librería para Consola en Python

`Console-Alertify` es una librería en Python que te permite mostrar mensajes en la consola con diferentes colores y formato. Ideal para proyectos donde desees agregar alertas, mensajes de éxito, advertencias y más, todo con colores personalizados.

[![License: MIT](https://black.readthedocs.io/en/stable/_static/license.svg)](https://github.com/psf/black/blob/main/LICENSE) 
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Características

- Muestra mensajes en consola con diferentes colores y fondos.
- Soporta la adición de la fecha y hora en los mensajes.
- Métodos para mostrar alertas, mensajes de éxito, advertencias, errores, etc.
- Limpieza de consola compatible con sistemas Windows y Unix.

## Instalación

Para instalar `Console-Console-Alertify`, simplemente usa pip:

```bash
pip install Console-Alertify
```

## Uso

A continuación se muestra cómo usar `Console-Alertify` en tu proyecto.

### Ejemplo Básico:

```python
import Console-Alertify

# Crear una instancia de la clase Console-Alertify
alert = Console-Alertify.Console-Alertify(time=True)

# Mostrar un mensaje de alerta
alert.Alerta("Este es un mensaje de alerta.")

# Mostrar un mensaje de éxito
alert.Exito("Operación exitosa!")

# Mostrar un mensaje de error
alert.Error("¡Algo salió mal!")

# Mostrar un mensaje de advertencia
alert.Warning("¡Cuidado! Algo podría ir mal.")

# Mostrar un mensaje informativo
alert.Informacion("Este es un mensaje informativo.")

# Limpiar la consola
alert.limpiar_consola()

# Imprimir una línea de color
alert.ColorLinea('verde', 50)
```

### Métodos Disponibles:

- `Alerta(mensaje: str)`: Muestra un mensaje de alerta en rojo.
- `Mensaje(mensaje: str)`: Muestra un mensaje normal.
- `Warning(mensaje: str)`: Muestra un mensaje de advertencia en amarillo.
- `Exito(mensaje: str)`: Muestra un mensaje de éxito en verde.
- `Error(mensaje: str)`: Muestra un mensaje de error en rojo con fondo rojo.
- `Informacion(mensaje: str)`: Muestra un mensaje informativo en cian.
- `Magenta(mensaje: str)`: Muestra un mensaje con fondo magenta y texto blanco.
- `limpiar_consola()`: Limpia la consola.
- `ColorLinea(color: str, longitud: int)`: Imprime una línea de color con la longitud especificada.

## Licencia

Este proyecto está bajo la Licencia MIT - consulta el archivo [LICENSE](LICENSE) para más detalles.

## Autor

Carlos Dev - [baa4tsdev@gmail.com](mailto:baa4tsdev@gmail.com)

Repositorio en GitHub: [https://github.com/Carlos-dev-G/Console-Alertify](https://github.com/Carlos-dev-G/Console-Alertify)
