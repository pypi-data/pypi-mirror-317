import boto3

class S3Manager:
    """Gestiona las operaciones de AWS S3."""
    
    def __init__(self, region_name="us-east-1"):
        """
        Inicializa el gestor de operaciones de S3 con un cliente S3 autenticado.

        Args:
            s3_client (boto3.client): Cliente autenticado de S3.
        """
        self.s3_client = boto3.client("s3", region_name=region_name)
    
    def upload_file_to_s3(self, file_path, bucket_name, s3_path):
        """
        Sube un archivo a un bucket de S3.

        Args:
            file_path (str): Ruta local del archivo a subir.
            bucket_name (str): Nombre del bucket S3.
            s3_path (str): Ruta dentro del bucket donde se almacenará el archivo.

        Returns:
            bool: `True` si el archivo fue subido exitosamente, `False` en caso contrario.
        """
        try:
            self.s3_client.upload_file(file_path, bucket_name, s3_path)
            print(f"Archivo subido exitosamente a {bucket_name}/{s3_path}")
            return True
        except Exception as e:
            print(f"Error al subir el archivo: {e}")
            return False
    
    def clear_s3_path(self, bucket_name, base_s3_path):
        """
        Elimina todos los archivos en la ruta especificada de un bucket de S3.

        Args:
            bucket_name (str): Nombre del bucket S3.
            base_s3_path (str): Ruta dentro del bucket para eliminar los archivos.

        Returns:
            None
        """
        try:
            response = self.s3_client.list_objects_v2(Bucket=bucket_name, Prefix=base_s3_path)
            if 'Contents' in response:
                objects_to_delete = [{'Key': obj['Key']} for obj in response['Contents']]
                self.s3_client.delete_objects(Bucket=bucket_name, Delete={'Objects': objects_to_delete})
                print(f"Ruta limpiada: s3://{bucket_name}/{base_s3_path}")
            else:
                print(f"No se encontraron archivos en la ruta: s3://{bucket_name}/{base_s3_path}")
        except Exception as e:
            print(f"Error al limpiar la ruta: {str(e)}")
