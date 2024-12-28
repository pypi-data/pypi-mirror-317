import os
import uuid
import pyarrow as pa
import pyarrow.parquet as pq
from datetime import datetime
from io import BytesIO
from googleapiclient.http import MediaFileUpload
from .s3 import S3Manager
from .config import ConfigManager
from .google import GoogleDriveManager
from dotenv import load_dotenv

config = ConfigManager()
s3_client = config.get_s3_client()
s3 = S3Manager(s3_client)

# Variables
load_dotenv()  # Carga las variables de entorno del archivo .env
credentials_path = os.getenv('CREDENTIALS_PATH')  # Ruta del archivo de credenciales

# Google Drive
gl = GoogleDriveManager(credentials_path)
service = gl.authenticate_google_drive()  # Autenticar en Google Drive



def save_to_s3_as_parquet(df, bucket_name, base_s3_path, overwrite=False):
    """
    Guarda un DataFrame como un archivo Parquet en S3, con opción de limpiar la ruta antes de guardar.

    Args:
        df (pd.DataFrame): El DataFrame que se desea guardar.
        bucket_name (str): El nombre del bucket de S3.
        base_s3_path (str): La ruta base en S3 donde se guardará el archivo.
        overwrite (bool): Si se debe limpiar la ruta antes de guardar el archivo (por defecto es False).

    Returns:
        None
    """
    # Añadir año, mes y día a la ruta base para una mayor organización
    now = datetime.now()
    full_s3_path = f"{base_s3_path}"
    
    # Si overwrite es True, se limpia la ruta en S3 antes de guardar el archivo
    if overwrite:
        s3.clear_s3_path(bucket_name, full_s3_path)
    
    # Generar un nombre único para el archivo
    s3_file_path = f"{full_s3_path}{generate_random_id()}.parquet"
    print(f"Guardando archivo en: s3://{bucket_name}/{s3_file_path}")
    
    # Convertir el DataFrame a Parquet en memoria
    table = pa.Table.from_pandas(df)
    buffer = BytesIO()
    pq.write_table(table, buffer)
    buffer.seek(0)  # Volver al principio del buffer
    
    # Subir el archivo Parquet a S3
    try:
        s3_client.upload_fileobj(buffer, bucket_name, s3_file_path)
        print(f"Archivo subido exitosamente a s3://{bucket_name}/{s3_file_path}")
    except Exception as e:
        print(f"Error al subir el archivo: {str(e)}")
    finally:
        # Cerrar el buffer después de la operación
        buffer.close()

def generate_random_id():
    """
    Genera un ID aleatorio (UUID) de versión 4.

    Returns:
        str: El ID aleatorio generado como string.
    """
    # Generar un UUID aleatorio
    random_id = uuid.uuid4()
    return str(random_id)

def upload_dataframe_to_drive(dataframe, file_name, parent_id, file_format='xlsx'):
    """
    Guarda un DataFrame en un archivo temporal y lo sube a Google Drive.

    Args:
        dataframe (pd.DataFrame): El DataFrame que se desea subir.
        file_name (str): Nombre del archivo que aparecerá en Google Drive.
        parent_id (str): ID de la carpeta en Google Drive donde se guardará el archivo.
        file_format (str): El formato en que se guardará el DataFrame ('csv' o 'xlsx'). Por defecto es 'xlsx'.

    Returns:
        str: El ID del archivo subido en Google Drive.
    """
    # Determinar la extensión del archivo y guardar el DataFrame localmente
    temp_file = f"{file_name}.{file_format}"
    try:
        # Guardar el DataFrame según el formato especificado
        if file_format == 'csv':
            dataframe.to_csv(temp_file, index=False)
        elif file_format == 'xlsx':
            dataframe.to_excel(temp_file, index=False)
        else:
            raise ValueError("Formato de archivo no soportado. Usa 'csv' o 'xlsx'.")

        # Metadatos del archivo para la subida a Google Drive
        file_metadata = {
            'name': f"{file_name}.{file_format}",
            'parents': [parent_id]
        }

        # Subir el archivo a Google Drive
        media = MediaFileUpload(temp_file, resumable=True)
        uploaded_file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        print(f"Archivo subido exitosamente. ID del archivo: {uploaded_file.get('id')}")
        return uploaded_file.get('id')
    except Exception as e:
        print(f"Ocurrió un error al subir el archivo: {e}")
    finally:
        # Asegurarse de que el archivo temporal se cierre correctamente antes de eliminarlo
        try:
            if os.path.exists(temp_file):
                os.remove(temp_file)
                print(f"Archivo temporal {temp_file} eliminado exitosamente.")
        except PermissionError as e:
            print(f"Error al eliminar el archivo temporal {temp_file}: {e}")

def create_drive_folder(folder_name, parent_id=None):
    """
    Crea una carpeta en Google Drive si no existe.

    Args:
        folder_name (str): Nombre de la carpeta que se desea crear.
        parent_id (str, optional): ID de la carpeta principal en la que se debe crear la nueva carpeta.
                                   Si no se proporciona, la carpeta se creará en la raíz.

    Returns:
        str: El ID de la carpeta creada o existente.
    """
    # Construir la consulta para buscar la carpeta existente
    query = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder'"
    if parent_id:
        query += f" and '{parent_id}' in parents"
    else:
        query += " and 'root' in parents"
    
    # Buscar la carpeta en Google Drive
    response = service.files().list(
        q=query,
        spaces='drive',
        fields='files(id, name)',
        pageSize=1
    ).execute()
    
    files = response.get('files', [])
    if files:
        # La carpeta ya existe
        folder_id = files[0]['id']
        print(f"La carpeta '{folder_name}' ya existe con ID: {folder_id}")
        return folder_id
    
    # La carpeta no existe, por lo que se crea
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
    }
    if parent_id:
        file_metadata['parents'] = [parent_id]
    
    folder = service.files().create(body=file_metadata, fields='id').execute()
    folder_id = folder.get('id')
    print(f"Carpeta '{folder_name}' creada con ID: {folder_id}")
    return folder_id


def create_today_structure_on_drive(parent_id=None):
    """
    Crea la estructura de carpetas para el día actual en Google Drive.
    Se crea una carpeta para el año, dentro de la cual se crea la carpeta para el mes
    y dentro de esta, la carpeta para el día.

    Args:
        parent_id (str, optional): ID de la carpeta principal donde se debe crear la estructura.
                                    Si no se proporciona, la estructura se creará en la raíz.

    Returns:
        str: El ID de la carpeta del día creada.
    """
    # Definir los meses en español
    months = [
        "01. Enero", "02. Febrero", "03. Marzo", "04. Abril",
        "05. Mayo", "06. Junio", "07. Julio", "08. Agosto",
        "09. Septiembre", "10. Octubre", "11. Noviembre", "12. Diciembre"
    ]

    # Obtener la fecha actual
    now = datetime.now()
    current_year = now.year
    current_month = now.month
    current_day = now.day

    # Obtener el nombre del mes actual en español
    current_month_name = months[current_month - 1]

    # Crear la carpeta del año
    year_folder_id = create_drive_folder(str(current_year), parent_id)

    # Crear la carpeta del mes dentro de la carpeta del año
    month_folder_id = create_drive_folder(current_month_name, year_folder_id)

    # Crear la carpeta del día dentro de la carpeta del mes
    return create_drive_folder(f"{current_day:02}", month_folder_id)
