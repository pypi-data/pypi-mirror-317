from nanoid import generate
from datetime import datetime

class IdManager:
    def __init__(self, longitud_aleatoria=6, formato_fecha="%Y%m%d"):
        """
        Inicializa la clase con los parámetros deseados.

        :param longitud_aleatoria: Longitud del sufijo aleatorio (predeterminado 6).
        :param formato_fecha: Formato de la fecha que se utilizará (predeterminado "%Y%m").
        """
        self.longitud_aleatoria = longitud_aleatoria
        self.formato_fecha = formato_fecha
        
    
    def generar_codigo(self):
        """
        Genera un código único utilizando el formato configurado.

        :return: Un código único basado en la fecha actual y una parte aleatoria.
        """
        # Obtener la fecha en el formato configurado
        fecha = datetime.now().strftime(self.formato_fecha)
        
        # Generar una parte aleatoria de letras y números
        parte_aleatoria = generate('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', self.longitud_aleatoria)
        
        # Concatenar la fecha con la parte aleatoria para formar el código final
        codigo = f"{fecha}_{parte_aleatoria}"
        
        return codigo
