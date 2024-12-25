import base64
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from queue import Queue

from googleapiclient.discovery import build

from google_py_apis.google_base_api import GoogleBaseAPI


class GmailAPI(GoogleBaseAPI):

    def __init__(self, email, base_dir, secret_key):
        super().__init__(email, base_dir, 'gmail_tokens', secret_key)
        self.scopes = [
            'https://mail.google.com/'
        ]
        self.__service = None

    def auth(self):
        super().auth(self.scopes)

    @property
    def service(self):
        if self.__service is None:
            self.__service = build('gmail', 'v1', credentials=self.credentials)
        return self.__service

    def list_labels(self):
        return self.service.users().labels().list(userId='me').execute()

    def get_label(self, label_id):
        return self.service.users().labels().get(userId='me', id=label_id).execute()

    def create_label(self, label, **kwargs):
        label_config = {
            'name': label,
            'type': 'user',
            'labelListVisibility': 'labelShow',
            'messageListVisibility': 'show',
            'messagesTotal': 0,
            'threadsUnread': 0,
            'messagesUnread': 0,
            'threadsTotal': 0,
            'color': {
                "textColor": '#000000',
                "backgroundColor": '#ffffff',
            }
        }
        for key, value in kwargs.items():
            label_config[key] = value
        return self.service.users().labels().create(userId='me', body=label_config).execute()

    def list_mails(
            self,
            query=None,
            max_pages=1,
            include_spam_and_trash=False
    ):
        messages = []

        page_num = 1
        page_token = None
        while page_num <= max_pages and (page_num == 1 or page_token is not None):
            response = self.service.users().messages().list(
                userId='me',
                q=query,
                pageToken=page_token,
                includeSpamTrash=include_spam_and_trash
            ).execute()

            messages_by_page = response.get('messages', None)
            if messages_by_page is not None:
                messages.extend(messages_by_page)

            page_token = response.get('nextPageToken', None)
            page_num += 1

        return messages

    def get_mail(self, mail_id):
        response = self.service.users().messages().get(userId='me', id=mail_id).execute()

        payloads_queue = Queue()
        payloads_queue.put(response.pop('payload', None))

        payloads = []
        while not payloads_queue.empty():

            payload = payloads_queue.get()
            if payload is None:
                continue

            # push parts to queue for further processing
            for part in payload.pop('parts', []):
                payloads_queue.put(part)

            # this part is done
            payloads.append(payload)

        response['payloads'] = payloads
        return response

    def add_remove_labels(self, mail_id, label_ids_add, label_ids_remove):
        return self.service.users().messages().modify(userId='me', id=mail_id, body={
            'removeLabelIds': label_ids_remove,
            'addLabelIds': label_ids_add
        }).execute()

    def send_to_unsubscribe(self, to, subject):
        text = ''
        msg = MIMEMultipart()
        msg['to'] = to
        msg['subject'] = subject
        msg.attach(MIMEText(text, 'plain'))
        raw_string = base64.urlsafe_b64encode(msg.as_bytes()).decode()

        sent_mail = self.service.users().messages().send(
            userId='me',
            body={
                'raw': raw_string
            }
        ).execute()

        send_mail_id = sent_mail['id']
        self.move_to_trash(send_mail_id)

    def move_to_trash(self, mail_id):
        self.service.users().messages().trash(userId='me', id=mail_id).execute()

    def download_attachment(self, mail_id, attachment_id, downloads_dir, filename=None):
        attachment = self.service.users().messages().attachments() \
            .get(userId='me', messageId=mail_id, id=attachment_id).execute()
        data = base64.urlsafe_b64decode(attachment['data'].encode('UTF-8'))

        if filename is not None:
            file_path = os.path.join(downloads_dir, mail_id, filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'wb') as fp:
                fp.write(data)

            return file_path
        else:
            return data
