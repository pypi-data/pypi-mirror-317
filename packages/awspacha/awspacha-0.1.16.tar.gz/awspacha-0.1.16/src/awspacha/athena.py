import boto3
import pandas as pd
from botocore.exceptions import BotoCoreError, ClientError


class AthenaManager:
    def __init__(self, region_name="us-east-1"):
        """
        Inicializa la clase AthenaManager.
        
        :param region_name: Región de AWS donde se encuentra Athena.
        """
        self.client = boto3.client("athena", region_name=region_name)

    def create_workgroup(self, name, description="", output_location=None):
        """
        Crea un workgroup (grupo de trabajo) en Athena.
        
        :param name: Nombre del workgroup.
        :param description: Descripción del workgroup.
        :param output_location: Ubicación en S3 donde se guardarán los resultados de las consultas.
        :return: Respuesta de la API create_work_group.
        """
        config = {
            "EnforceWorkGroupConfiguration": False,
            "PublishCloudWatchMetricsEnabled": True,
        }
        if output_location:
            config["ResultConfiguration"] = {"OutputLocation": output_location}

        try:
            response = self.client.create_work_group(
                Name=name,
                Description=description,
                Configuration=config
            )
            print(f"Workgroup '{name}' creado exitosamente.")
            return response
        except ClientError as e:
            print(f"Error al crear el workgroup: {e}")
            return None

    def get_workgroup(self, name):
        """
        Obtiene los detalles de un workgroup en Athena.
        
        :param name: Nombre del workgroup.
        :return: Detalles del workgroup.
        """
        try:
            response = self.client.get_work_group(WorkGroup=name)
            return response
        except ClientError as e:
            print(f"Error al obtener el workgroup: {e}")
            return None

    def update_workgroup(self, name, description=None, output_location=None):
        """
        Actualiza un workgroup en Athena.
        
        :param name: Nombre del workgroup.
        :param description: Nueva descripción para el workgroup.
        :param output_location: Nueva ubicación en S3 para los resultados de las consultas.
        :return: Respuesta de la API update_work_group.
        """
        updates = {}
        if description:
            updates["Description"] = description
        if output_location:
            updates["ConfigurationUpdates"] = {
                "ResultConfigurationUpdates": {"OutputLocation": output_location}
            }

        try:
            response = self.client.update_work_group(
                WorkGroup=name,
                **updates
            )
            print(f"Workgroup '{name}' actualizado exitosamente.")
            return response
        except ClientError as e:
            print(f"Error al actualizar el workgroup: {e}")
            return None

    def delete_workgroup(self, name):
        """
        Elimina un workgroup en Athena.
        
        :param name: Nombre del workgroup a eliminar.
        :return: Respuesta de la API delete_work_group.
        """
        try:
            response = self.client.delete_work_group(
                WorkGroup=name,
                RecursiveDeleteOption=True
            )
            print(f"Workgroup '{name}' eliminado exitosamente.")
            return response
        except ClientError as e:
            print(f"Error al eliminar el workgroup: {e}")
            return None

    def execute_query(self, query, database, output_location):
        """
        Ejecuta una consulta SQL en Athena.
        
        :param query: Consulta SQL a ejecutar.
        :param database: Nombre de la base de datos en Athena.
        :param output_location: Ubicación en S3 para almacenar los resultados de la consulta.
        :return: ID de ejecución de la consulta.
        """
        try:
            response = self.client.start_query_execution(
                QueryString=query,
                QueryExecutionContext={"Database": database},
                ResultConfiguration={"OutputLocation": output_location}
            )
            execution_id = response["QueryExecutionId"]
            print(f"Consulta iniciada exitosamente con ID de ejecución: {execution_id}")
            return execution_id
        except ClientError as e:
            print(f"Error al ejecutar la consulta: {e}")
            return None

    def get_query_results(self, execution_id):
        """
        Recupera los resultados de una consulta ejecutada en Athena.
        
        :param execution_id: ID de ejecución de la consulta.
        :return: Resultados de la consulta.
        """
        try:
            response = self.client.get_query_results(QueryExecutionId=execution_id)
            return response
        except ClientError as e:
            print(f"Error al recuperar los resultados de la consulta: {e}")
            return None

    def get_query_results_as_dataframe(self, execution_id, s3_output_location):
        """
        Recupera los resultados de una consulta ejecutada en Athena como un DataFrame.

        :param execution_id: ID de ejecución de la consulta.
        :param s3_output_location: Ubicación en S3 donde se encuentran los resultados de la consulta.
        :return: DataFrame de Pandas con los resultados.
        """
        try:
            # Construir la ruta del archivo en S3 con el ID de ejecución
            result_file = f"{s3_output_location}/{execution_id}.csv"
            # Leer el archivo directamente como un DataFrame
            df = pd.read_csv(result_file, dtype='str')
            print("Resultados de la consulta cargados exitosamente en un DataFrame.")
            return df
        except Exception as e:
            print(f"Error al cargar los resultados en un DataFrame: {e}")
            return None