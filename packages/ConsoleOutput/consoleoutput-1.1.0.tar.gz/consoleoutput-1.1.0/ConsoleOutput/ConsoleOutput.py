from datetime import datetime


class Color:
    F_COLOR = {
        "NE": "\033[30m",  # Negro
        "RO": "\033[31m",  # Rojo
        "VE": "\033[32m",  # Verde
        "AM": "\033[33m",  # Amarillo
        "AZ": "\033[34m",  # Azul
        "MA": "\033[35m",  # Magenta
        "CI": "\033[36m",  # Cian
        "BL": "\033[37m",  # Blanco
    }

    B_COLOR = {
        "NE": "\033[40m",  # Fondo negro
        "RO": "\033[41m",  # Fondo rojo
        "VE": "\033[42m",  # Fondo verde
        "AM": "\033[43m",  # Fondo amarillo
        "AZ": "\033[44m",  # Fondo azul
        "MA": "\033[45m",  # Fondo magenta
        "CI": "\033[46m",  # Fondo cian
        "BL": "\033[47m",  # Fondo blanco
    }

    @staticmethod
    def reset():
        return "\033[0m"  # Reset color


class SalidaConsola:
    @staticmethod
    def imprimir(texto: str, color_texto: str = "BL", color_fondo: str = "NE"):
        # Obtener los colores de texto y fondo
        color_texto = Color.F_COLOR.get(color_texto, Color.F_COLOR["BL"])
        color_fondo = Color.B_COLOR.get(color_fondo, Color.B_COLOR["NE"])
        print(f'{color_fondo}{color_texto}{texto}{Color.reset()}')

    class Alertas:
        def __init__(self, time: bool = True):
            self.time = time
            self.color = Color()

        @staticmethod
        def get_time():
            hora_actual = datetime.now()
            return hora_actual.strftime("[%H:%M:%S]")  # Corregir formato a %H:%M:%S

        @staticmethod
        def ajustar_mensaje(etiqueta: str):
            # Ajustar el texto de la etiqueta a 15 caracteres
            return f"[ ! {etiqueta:^13} ! ]"  # Centrado con espacios

        def Danger(self, text: str):
            etiqueta = self.ajustar_mensaje("DANGER")
            if self.time:
                mensaje = f"{self.color.B_COLOR.get('RO')}{self.color.F_COLOR.get('AM')}{etiqueta} {self.color.reset()} {self.get_time()} {self.color.B_COLOR.get('RO')}{self.color.F_COLOR.get('AM')} {text} {self.color.reset()}"
            else:
                mensaje = f"{self.color.B_COLOR.get('RO')}{self.color.F_COLOR.get('AM')}{etiqueta} {self.color.reset()} {text} {self.color.reset()}"
            print(mensaje)

        def Risk(self, text: str):
            etiqueta = self.ajustar_mensaje("RISK")
            if self.time:
                mensaje = f"{self.color.B_COLOR.get('AM')}{self.color.F_COLOR.get('RO')}{etiqueta} {self.color.reset()} {self.get_time()} {self.color.B_COLOR.get('AM')}{self.color.F_COLOR.get('RO')} {text} {self.color.reset()}"
            else:
                mensaje = f"{self.color.B_COLOR.get('AM')}{self.color.F_COLOR.get('RO')}{etiqueta} {self.color.reset()} {text} {self.color.reset()}"
            print(mensaje)

        def Warning(self, text: str):
            etiqueta = self.ajustar_mensaje("WARNING")
            if self.time:
                mensaje = f"{self.color.B_COLOR.get('VE')}{self.color.F_COLOR.get('CI')}{etiqueta} {self.color.reset()} {self.get_time()} {self.color.B_COLOR.get('VE')}{self.color.F_COLOR.get('CI')} {text} {self.color.reset()}"
            else:
                mensaje = f"{self.color.B_COLOR.get('VE')}{self.color.F_COLOR.get('CI')}{etiqueta} {self.color.reset()} {text} {self.color.reset()}"
            print(mensaje)

        def Normal(self, text: str):
            etiqueta = self.ajustar_mensaje("NORMAL")
            if self.time:
                mensaje = f"{self.color.B_COLOR.get('NE')}{self.color.F_COLOR.get('BL')}{etiqueta} {self.color.reset()} {self.get_time()} {self.color.B_COLOR.get('NE')}{self.color.F_COLOR.get('BL')} {text} {self.color.reset()}"
            else:
                mensaje = f"{self.color.B_COLOR.get('NE')}{self.color.F_COLOR.get('BL')}{etiqueta} {self.color.reset()} {text} {self.color.reset()}"
            print(mensaje)

        def Message(self, text: str):
            etiqueta = self.ajustar_mensaje("MESSAGE")
            if self.time:
                mensaje = f"{self.color.B_COLOR.get('BL')}{self.color.F_COLOR.get('CI')}{etiqueta} {self.color.reset()} {self.get_time()} {self.color.B_COLOR.get('BL')}{self.color.F_COLOR.get('CI')} {text} {self.color.reset()}"
            else:
                mensaje = f"{self.color.B_COLOR.get('BL')}{self.color.F_COLOR.get('CI')}{etiqueta} {self.color.reset()} {text} {self.color.reset()}"
            print(mensaje)

        def Information(self, text: str):
            etiqueta = self.ajustar_mensaje("INFORMATION")
            if self.time:
                mensaje = f"{self.color.B_COLOR.get('AZ')}{self.color.F_COLOR.get('VE')}{etiqueta} {self.color.reset()} {self.get_time()} {self.color.B_COLOR.get('AZ')}{self.color.F_COLOR.get('VE')} {text} {self.color.reset()}"
            else:
                mensaje = f"{self.color.B_COLOR.get('AZ')}{self.color.F_COLOR.get('VE')}{etiqueta} {self.color.reset()} {text} {self.color.reset()}"
            print(mensaje)