import boto3  # Usamos boto3 para interactuar con AWS Glue
from botocore.exceptions import ClientError  # Para manejar errores de AWS

class CrawlerManager:
    """
    Clase para administrar los Crawlers de AWS Glue.

    Esta clase proporciona métodos para crear, eliminar, iniciar, detener y obtener información sobre crawlers.
    """

    def __init__(self, region_name='us-east-1'):
        """
        Inicializa el objeto GlueCrawlerManager.

        :param region_name: La región de AWS donde se encuentra el servicio de Glue (por defecto 'us-east-1').
        """
        # Creamos un cliente de Glue usando boto3
        self.client = boto3.client('glue', region_name=region_name)

    def create_crawler(self, name, role, database_name, s3_target_path):
        """
        Crea un nuevo crawler en AWS Glue.

        :param name: Nombre del crawler.
        :param role: ARN del rol de IAM que el crawler usará.
        :param database_name: Nombre de la base de datos de destino en Glue.
        :param s3_target_path: Ruta de S3 donde el crawler buscará los datos.
        """
        try:
            # Creamos el crawler en AWS Glue
            response = self.client.create_crawler(
                Name=name,
                Role=role,
                DatabaseName=database_name,
                Targets={
                    's3Targets': [
                        {
                            'Path': s3_target_path,
                        },
                    ],
                },
            )
            print(f"Crawler {name} creado exitosamente.")
        except ClientError as e:
            print(f"Error al crear el crawler {name}: {e}")

    def start_crawler(self, name):
        """
        Inicia un crawler que ya ha sido creado en AWS Glue.

        :param name: Nombre del crawler a iniciar.
        """
        try:
            # Iniciamos el crawler en AWS Glue
            response = self.client.start_crawler(Name=name)
            print(f"Crawler {name} iniciado exitosamente.")
        except ClientError as e:
            print(f"Error al iniciar el crawler {name}: {e}")

    def stop_crawler(self, name):
        """
        Detiene un crawler que se está ejecutando en AWS Glue.

        :param name: Nombre del crawler a detener.
        """
        try:
            # Detenemos el crawler en AWS Glue
            response = self.client.stop_crawler(Name=name)
            print(f"Crawler {name} detenido exitosamente.")
        except ClientError as e:
            print(f"Error al detener el crawler {name}: {e}")

    def delete_crawler(self, name):
        """
        Elimina un crawler de AWS Glue.

        :param name: Nombre del crawler a eliminar.
        """
        try:
            # Eliminamos el crawler en AWS Glue
            response = self.client.delete_crawler(Name=name)
            print(f"Crawler {name} eliminado exitosamente.")
        except ClientError as e:
            print(f"Error al eliminar el crawler {name}: {e}")

    def get_crawler_status(self, name):
        """
        Obtiene el estado de un crawler en AWS Glue.

        :param name: Nombre del crawler.
        :return: El estado del crawler.
        """
        try:
            # Obtenemos el estado del crawler
            response = self.client.get_crawler(Name=name)
            status = response['Crawler']['State']
            print(f"El estado del crawler {name} es: {status}")
        except ClientError as e:
            print(f"Error al obtener el estado del crawler {name}: {e}")
