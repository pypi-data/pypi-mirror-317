from datetime import datetime
import os


class ConsoleAlertify:
    """
    Clase Consola para mostrar mensajes en la consola con diferentes colores y formato.
    """

    # Definir un diccionario para colores de texto y fondo
    COLORES = {
        'rojo': '\033[31m',
        'amarillo': '\033[33m',
        'verde': '\033[32m',
        'cian': '\033[36m',
        'magenta': '\033[35m',
        'blanco': '\033[37m',
        'negro': '\033[30m',
        'fondo_rojo': '\033[41m',
        'fondo_amarillo': '\033[43m',
        'fondo_verde': '\033[42m',
        'fondo_cian': '\033[46m',
        'fondo_magenta': '\033[45m',
        'fondo_blanco': '\033[47m',
        'fondo_negro': '\033[40m',
        'fondo_azul': '\033[44m',
    }

    def __init__(self, time: bool = True):
        """
        Inicializa la clase Consola.

        Parámetros:
        time (bool): Si es True, los mensajes mostrarán la fecha y hora actuales.
        """
        self.time = time

    def __TIME(self):
        """Devuelve la fecha y hora actual si 'time' es True."""
        return (
            f"[{datetime.now().strftime('%Y/%m/%d %H:%M:%S')}] "
            if self.time
            else ""
        )

    def __BRACKET_LEFT(self, code: str, background_code: str) -> str:
        """Genera el formato de color y fondo para el mensaje."""
        return (
            f"{self.COLORES.get(background_code, self.COLORES['fondo_negro'])}"
            f"{self.COLORES.get('blanco')}[{code}]\033[0m"
        )

    def __Texto(self, text: str, color: str) -> str:
        """Retorna el texto coloreado."""
        return (
            f"{self.COLORES.get(color, self.COLORES['blanco'])}{text}\033[0m"
        )

    @staticmethod
    def limpiar_consola():
        """Limpia la consola según el sistema operativo."""
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def ColorLinea(color: str, longitud: int):
        """
        Imprime una línea de color con la longitud especificada.
        """
        print(
            f"{Alertify.COLORES.get(color, Alertify.COLORES['fondo_negro'])}"
            + " " * longitud
            + '\033[0m'
        )

    def _log(self, type_: str, color: str, background: str, mensaje: str):
        """Método genérico para imprimir mensajes formateados."""
        bracket = self.__BRACKET_LEFT(self.__Texto(type_, color), background)
        print(f"{bracket} {self.__TIME()} {self.__Texto(mensaje, color)}")

    def Alerta(self, mensaje: str):
        """Imprime un mensaje de alerta."""
        self._log("ALERTA", 'rojo', 'fondo_rojo', mensaje)

    def Mensaje(self, mensaje: str):
        """Imprime un mensaje normal."""
        self._log("MENSAJE", 'blanco', 'fondo_negro', mensaje)

    def Warning(self, mensaje: str):
        """Imprime un mensaje de advertencia."""
        self._log("ADVERTENCIA", 'amarillo', 'fondo_amarillo', mensaje)

    def Exito(self, mensaje: str):
        """Imprime un mensaje de éxito."""
        self._log("EXITO", 'verde', 'fondo_verde', mensaje)

    def Error(self, mensaje: str):
        """Imprime un mensaje de error."""
        self._log("ERROR", 'rojo', 'fondo_rojo', mensaje)

    def Informacion(self, mensaje: str):
        """Imprime un mensaje informativo."""
        self._log("INFORMACION", 'cian', 'fondo_cian', mensaje)

    def Magenta(self, mensaje: str):
        """Imprime un mensaje con fondo magenta y texto blanco."""
        self._log("MAGENTA", 'magenta', 'fondo_magenta', mensaje)
