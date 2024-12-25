import json
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from google_py_apis import util


class GoogleBaseAPI:

    def __init__(self, email, base_dir, tokens_dirname, tokens_secret_key):
        self.req_email = email
        self.credentials = None
        self.__userinfo_service = None
        self.__email = None
        self.scopes_base = ['https://www.googleapis.com/auth/userinfo.email']
        self.base_dir = base_dir
        self.tokens_dirname = tokens_dirname
        self.tokens_secret_key = tokens_secret_key

    @property
    def userinfo_service(self):
        if self.__userinfo_service is None:
            self.__userinfo_service = build('oauth2', 'v2', credentials=self.credentials)

        return self.__userinfo_service

    @property
    def email(self):
        if self.__email is None:
            self.__email = self.userinfo_service.userinfo().get().execute()['email']
        return self.__email

    def auth(self, scopes):
        os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

        scopes.extend(self.scopes_base)
        tokens_path = os.path.join(self.base_dir, f'{self.tokens_dirname}/{self.req_email}.json')

        desktop_credentials_path = os.path.join(self.base_dir, 'config', 'desktop_credentials.json')

        self.credentials = None
        # if token already exists
        if os.path.exists(tokens_path):
            with open(tokens_path, 'r') as f:
                info_str_encrypted = f.read()
                info_str_decrypted = util.decrypt_text(info_str_encrypted, self.tokens_secret_key)
                if info_str_decrypted is not None:
                    info = json.loads(info_str_decrypted)
                    self.credentials = Credentials.from_authorized_user_info(info, scopes)
                else:
                    raise Exception(
                        'Unable to decrypt tokens. Make sure key is correct or re-authenticate after clearing the tokens in cache.')

        # if not exists or invalid
        if not self.credentials or not self.credentials.valid:
            # init auth flow
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(desktop_credentials_path, scopes)
                self.credentials = flow.run_local_server(port=0)

        if self.req_email != self.email:

            if os.path.exists(tokens_path):
                # clear the tokens since they most likely tinkered with
                os.remove(tokens_path)

            raise Exception(
                f'Requested email [{self.req_email}] does not match authenticated email [{self.email}].')
        else:
            tokens_path = os.path.join(self.base_dir, f'{self.tokens_dirname}/{self.email}.json')
            os.makedirs(os.path.dirname(tokens_path), exist_ok=True)
            with open(tokens_path, 'w') as token:
                dump_str_decrypted = self.credentials.to_json()
                dump_str_encrypted = util.encrypt_text(dump_str_decrypted, self.tokens_secret_key)
                if dump_str_encrypted is not None:
                    token.write(dump_str_encrypted)
                else:
                    raise Exception("Unable to encrypt tokens.")
