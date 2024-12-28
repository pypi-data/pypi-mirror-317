class SQLFileManager:
    """
    Clase para gestionar archivos SQL y personalizar consultas con parámetros dinámicos.
    """

    def __init__(self, path='.env'):
        """
        Inicializa el administrador con la ruta del archivo SQL.
        
        :param path: Ruta del archivo SQL.
        """
        self.path = path

    def read_and_format(self,path, **kwargs):
        """
        Lee el archivo SQL y personaliza la consulta con los parámetros proporcionados.
        
        :param kwargs: Diccionario de parámetros para formatear la consulta.
        :return: Cadena de consulta SQL personalizada.
        """
        try:
            with open(path, 'r', encoding='utf-8') as file:
                sql_query = file.read()
                return sql_query.format(**kwargs)
        except FileNotFoundError:
            raise FileNotFoundError(f"El archivo SQL en {path} no se encontró.")
        except KeyError as e:
            raise ValueError(f"Falta el parámetro necesario para formatear la consulta: {e}")
        except Exception as e:
            raise Exception(f"Ocurrió un error al procesar el archivo SQL: {e}")
