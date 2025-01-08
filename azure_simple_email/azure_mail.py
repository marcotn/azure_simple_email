import base64
import mimetypes
import os
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import msal
import requests
class AzureSendMail:

    def __init__(self, user_id):
        self.to = []
        self.cc = []
        self.bcc = []
        self.attachments = []
        self.user_id = user_id
        self.endpoint = f'https://graph.microsoft.com/v1.0/users/{self.user_id}/sendMail'

    def add_recipient(self, recipient: str):
        self.to.append(recipient)

    def add_cc_recipient(self, recipient: str):
        self.cc.append(recipient)

    def add_ccn_recipient(self, recipient: str):
        self.bcc.append(recipient)

    def add_attachment(self, filename: str):
        b64_content = base64.b64encode(open(filename, 'rb').read())
        mime_type = mimetypes.guess_type(filename)[0]
        mime_type = mime_type if mime_type else ''
        self.attachments.append(
            {'@odata.type': '#microsoft.graph.fileAttachment',
             'ContentBytes': b64_content.decode('utf-8'),
             'ContentType': mime_type,
             'Name': filename})
        return True

    def add_attachment_io(self, content: bytes, filename: str):
        b64_content = base64.b64encode(content)
        mime_type = mimetypes.guess_type(filename)[0]
        mime_type = mime_type if mime_type else ''
        self.attachments.append(
            {'@odata.type': '#microsoft.graph.fileAttachment',
             'ContentBytes': b64_content.decode('utf-8'),
             'ContentType': mime_type,
             'Name': filename})
        return True


    def get_token(self):
        client_id = os.environ.get('AZURE_EMAIL_CLIENT_ID')
        client_secret = os.environ.get('AZURE_EMAIL_CLIENT_SECRET')
        authority = os.environ.get('AZURE_EMAIL_CLIENT_AUTHORITY')


        app = msal.ConfidentialClientApplication(
            client_id=client_id,
            client_credential=client_secret,
            authority=authority)

        scopes = ["https://graph.microsoft.com/.default"]

        result = app.acquire_token_silent(scopes, account=None)

        if not result:
            print(
                "No suitable token exists in cache. Let's get a new one from Azure Active Directory.")
            result = app.acquire_token_for_client(scopes=scopes)

        return result

    def create_message(self, sender, subject, content):

        message = MIMEMultipart("alternative")
        _html = MIMEText(content, "html")
        message.attach(_html)
        message['to'] = self.to[0]
        message['cc'] = ','.join(self.cc)
        message['bcc'] = ','.join(self.bcc)
        message['from'] = sender
        message['subject'] = subject
        raw = base64.b64encode(message.as_bytes())
        #raw = base64.urlsafe_b64encode(message.as_bytes())
        return raw.decode()


    def send_mail_mime_types(self, subject: str, content: str):
        result = self.get_token()
        if "access_token" in result:
            email_msg = self.create_message(sender=self.user_id,  subject=subject, content=content)
            headers = {'Authorization': 'Bearer ' + result['access_token']}
            headers['Content-Type'] = 'text/plain'
            r = requests.post(self.endpoint,
                          headers=headers, data=email_msg)
            if r.ok:
                return {'result': 'ok'}
            else:
                return {'result': 'ko', 'error': r.json()}
        else:
            print(result.get("error"))
            print(result.get("error_description"))
            print(result.get("correlation_id"))


    def send_email(self, subject: str, text: str, content_type='Text'):
        """Sends Out The actual email
           Parameters:
           subject string
           test string
           content_type string (either "text" ot "html")
        """
        result = self.get_token()
        if "access_token" in result:
            email_msg = {'Message': {'Subject': subject,
                                     'Body': {'ContentType': content_type, 'Content': text},
                                     'toRecipients': [{'EmailAddress': {'Address': _email}} for _email in self.to],
                                     'ccRecipients': [{'EmailAddress': {'Address': _email}} for _email in self.cc],
                                     'bccRecipients': [{'EmailAddress': {'Address': _email}} for _email in self.bcc],
                                     'Attachments': self.attachments
                                     },
                         'SaveToSentItems': 'true'}
            r = requests.post(self.endpoint,
                              headers={'Authorization': 'Bearer ' + result['access_token']}, json=email_msg)
            if r.ok:
                return {'result': 'ok'}
            else:

                return {'result': 'ko', 'error': r.text}
        else:
            print(result.get("error"))
            print(result.get("error_description"))
            print(result.get("correlation_id"))