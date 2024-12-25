import mimetypes
import os.path

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from google_py_apis.google_base_api import GoogleBaseAPI


class GoogleDriveAPI(GoogleBaseAPI):
    def __init__(self, email, base_dir, secret_key):
        super().__init__(email, base_dir, 'gdrive_tokens', secret_key)
        self.scopes = [
            'https://www.googleapis.com/auth/drive',
        ]
        self.__service = None

        # This will be a mapping like : (parent_folder_id, folder_name) -> folder_id
        # parent_folder_id = None will indicate root (My Drive)
        self.path_to_folder_id_map = dict()

    def auth(self):
        super().auth(self.scopes)

    @property
    def service(self):
        if self.__service is None:
            self.__service = build("drive", "v3", credentials=self.credentials)
        return self.__service

    def __find_path_id(self, path, parent_folder_id=None, create_if_missing=False):
        path_folder_id = None
        nodes = [i for i in path.split('/') if len(i.strip()) > 0]
        for node in nodes:
            cached = self.path_to_folder_id_map.get((parent_folder_id, node), None)
            if cached:
                path_folder_id = cached
                print(f'Found folder id {path_folder_id} for {node} within {parent_folder_id}')
                parent_folder_id = path_folder_id
                continue

            print(f'Querying to fetch folder id for {node} within {parent_folder_id}')

            query = f"name='{node}' and mimeType='application/vnd.google-apps.folder'"
            if parent_folder_id:
                query += f" and '{parent_folder_id}' in parents"

            results = self.service.files().list(q=query, fields="files(id, name)").execute()
            folders = results.get('files', [])

            if folders:
                assert len(folders) == 1
                path_folder_id = folders[0]['id']
                self.path_to_folder_id_map[(parent_folder_id, node)] = path_folder_id
                parent_folder_id = path_folder_id
            elif create_if_missing:
                folder_metadata = {
                    'name': node,
                    'mimeType': 'application/vnd.google-apps.folder',
                }
                if parent_folder_id:
                    folder_metadata['parents'] = [parent_folder_id]
                folder = self.service.files().create(body=folder_metadata, fields='id').execute()
                path_folder_id = folder['id']
                self.path_to_folder_id_map[(parent_folder_id, node)] = path_folder_id
                parent_folder_id = path_folder_id
            else:
                path_folder_id = None

            if path_folder_id is None:
                break

        return path_folder_id

    def upload_file(self, file_path, dest_dir=None):
        parent_folder_id = None
        if dest_dir is not None and len(dest_dir) > 0:
            parent_folder_id = self.__find_path_id(dest_dir, create_if_missing=True)

        file_name = os.path.basename(file_path)
        mime_type, _ = mimetypes.guess_type(file_path)

        file_metadata = {'name': file_name}
        if parent_folder_id:
            file_metadata['parents'] = [parent_folder_id]

        media = MediaFileUpload(file_path, mimetype=mime_type)

        file = self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id',
        ).execute()

        file_id = file.get("id")
        print(file_id)

        return file_id
