import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.service_account import Credentials

class GoogleDriveManager:
    """Gestiona las operaciones de Google Drive."""
    
    def __init__(self, credentials_path):
        """
        Inicializa el gestor de Google Drive con la ruta de las credenciales.

        Args:
            credentials_path (str): Ruta del archivo de credenciales de Google.
        """
        self.credentials_path = credentials_path
        self.service = self.authenticate_google_drive()  # Autenticación en Google Drive
    
    def authenticate_google_drive(self):
        """
        Autentica el acceso a Google Drive usando el archivo de credenciales.

        Returns:
            googleapiclient.discovery.Resource: Servicio autenticado de Google Drive.
        """
        creds = Credentials.from_service_account_file(
            self.credentials_path, 
            scopes=["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/drive.readonly"]
        )
        return build('drive', 'v3', credentials=creds)
    
    def get_file_name(self, file_id):
        """
        Obtiene el nombre de un archivo de Google Drive usando su ID.

        Args:
            file_id (str): ID del archivo en Google Drive.

        Returns:
            str: Nombre del archivo.
        """
        file = self.service.files().get(fileId=file_id, fields='name').execute()
        return file.get('name')
    
    def download_file(self, file_id, file_name):
        """
        Descarga un archivo desde Google Drive y lo guarda en el directorio local.

        Args:
            file_id (str): ID del archivo en Google Drive.
            file_name (str): Nombre con el que se guardará el archivo localmente.

        Returns:
            str: Ruta al archivo descargado.
        """
        request = self.service.files().get_media(fileId=file_id)
        with io.FileIO(file_name, 'wb') as fh:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print(f"Descargando {int(status.progress() * 100)}%.")
        return file_name
