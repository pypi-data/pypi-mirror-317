import os
import boto3
from dotenv import load_dotenv

class ConfigManager:
    """Gestiona la configuración y las variables de entorno."""
    
    def __init__(self):
        """
        Inicializa el gestor de configuración y carga las variables de entorno desde el archivo .env.
        """
        load_dotenv()  # Carga las variables de entorno del archivo .env
        self.credentials_path = os.getenv('CREDENTIALS_PATH')  # Ruta del archivo de credenciales
        self.aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')  # ID de la clave de acceso de AWS
        self.aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')  # Clave de acceso secreta de AWS
        self.region_name = os.getenv('AWS_DEFAULT_REGION')  # Región de AWS
    
    def get_s3_client(self):
        """
        Inicializa y retorna un cliente de S3 con las credenciales de AWS.

        Returns:
            boto3.client: Cliente S3 autenticado.
        """
        return boto3.client(
            's3',
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region_name
        )
