import logging
import boto3

class GlueManager:
    """
    Clase para gestionar operaciones relacionadas con AWS Glue y S3.
    """
    def __init__(self):
        """
        Inicializa el cliente de S3 y configura el logger.
        """
        self.logger = logging.getLogger(__name__)
        self.s3_client = boto3.client('s3')

    def clean_folder(self, bucket_name, prefix):
        """
        Limpia una carpeta en S3 eliminando objetos en el prefijo especificado.

        :param bucket_name: Nombre del bucket S3.
        :param prefix: Prefijo de la carpeta a limpiar.
        """
        try:
            # Listar y preparar los objetos para eliminar
            objects_to_delete = [
                {'Key': obj['Key']} 
                for obj in self.s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix).get('Contents', []) 
                if not obj['Key'].endswith('/')
            ]
            if objects_to_delete:
                # Eliminar los objetos seleccionados
                self.s3_client.delete_objects(Bucket=bucket_name, Delete={'Objects': objects_to_delete})
                self.logger.info(f"Se eliminaron {len(objects_to_delete)} objetos de {bucket_name}/{prefix}")
        except Exception as e:
            self.logger.error(f"Error al limpiar la carpeta {bucket_name}/{prefix}: {e}")
            raise

    def get_table_from_source(self, spark, url, user, password, query):
        """
        Lee una tabla desde una fuente JDBC.

        :param spark: Instancia de SparkSession.
        :param url: URL de conexión a la base de datos.
        :param user: Usuario de la base de datos.
        :param password: Contraseña del usuario.
        :param query: Consulta SQL para extraer los datos.
        :return: DataFrame de Spark.
        """
        try:
            return spark.read.format("jdbc") \
                .option("url", url) \
                .option("user", user) \
                .option("password", password) \
                .option("query", query) \
                .load()
        except Exception as e:
            self.logger.error(f"Error al leer la tabla desde la fuente: {e}")
            raise

    def write_to_s3(self, DynamicFrame, glue_context, df, output_bucket, output_prefix):
        """
        Escribe un DataFrame en formato Glue Parquet en S3.

        :param DynamicFrame: Dynamic Frame.
        :param glue_context: Contexto de AWS Glue.
        :param df: DataFrame de Spark.
        :param output_bucket: Nombre del bucket de salida.
        :param output_prefix: Prefijo de la carpeta de salida.
        """
        try:
            # Convertir el DataFrame en un DynamicFrame
            glue_df = DynamicFrame.fromDF(df, glue_context, "df")
            output_path = f"s3://{output_bucket}/{output_prefix}/"

            # Limpiar la carpeta antes de escribir
            self.clean_folder(output_bucket, output_prefix)

            # Escribir en S3 en formato Glue Parquet
            glue_context.write_dynamic_frame.from_options(
                frame=glue_df,
                connection_type="s3",
                connection_options={"path": output_path},
                format="glueparquet"
            )
            self.logger.info(f"Datos escritos exitosamente en {output_path}")
        except Exception as e:
            self.logger.error(f"Error al escribir los datos en S3: {e}")
            raise
