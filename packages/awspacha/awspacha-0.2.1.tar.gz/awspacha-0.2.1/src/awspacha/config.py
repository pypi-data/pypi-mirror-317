import os
import boto3
from dotenv import load_dotenv

class ConfigManager:
    """Gestiona la configuración y las variables de entorno."""
    
    def __init__(self, region_name = 'us-east-1'):
        """
        Inicializa el gestor de configuración y carga las variables de entorno desde el archivo .env.
        """
        load_dotenv()  # Carga las variables de entorno del archivo .env
        self.credentials_path = os.getenv('CREDENTIALS_PATH')  # Ruta del archivo de credenciales
        self.aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')  # ID de la clave de acceso de AWS
        self.aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')  # Clave de acceso secreta de AWS
        self.region_name = region_name  # Región de AWS
    
    def get_s3_client(self):
        """
        Inicializa y retorna un cliente de S3 utilizando las credenciales disponibles.
        Si no se encuentran credenciales explícitas, usa las predeterminadas del sistema.

        Returns:
            boto3.client: Cliente S3 autenticado.
        """
        if self.aws_access_key_id and self.aws_secret_access_key:
            # Si las credenciales están disponibles, las usamos explícitamente
            return boto3.client(
                's3',
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                region_name=self.region_name
            )
        else:
            # Si no hay credenciales explícitas, boto3 usará las predeterminadas
            return boto3.client('s3', region_name=self.region_name)