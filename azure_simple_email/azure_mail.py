import base64
import mimetypes
import os
import msal
import requests

class AzureSendMail:

    def __init__(self, user_id):
        self.to = []
        self.attachments = []
        self.user_id = user_id

    def add_recipient(self, recipient: str):
        self.to.append(recipient)

    def add_attachment(self, filename: str):
        try:
            b64_content = base64.b64encode(open(filename, 'rb').read())
            mime_type = mimetypes.guess_type(filename)[0]
            mime_type = mime_type if mime_type else ''
            self.attachments.append(
                {'@odata.type': '#microsoft.graph.fileAttachment',
                 'ContentBytes': b64_content.decode('utf-8'),
                 'ContentType': mime_type,
                 'Name': filename})
        except:
            return False
        return True

    def send_email(self, subject: str, text: str):
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

        if "access_token" in result:
            endpoint = f'https://graph.microsoft.com/v1.0/users/{self.user_id}/sendMail'
            email_msg = {'Message': {'Subject': subject,
                                     'Body': {'ContentType': 'Text', 'Content': text},
                                     'ToRecipients': [{'EmailAddress': {'Address': _email}} for _email in self.to],
                                     'Attachments': self.attachments
                                     },
                         'SaveToSentItems': 'true'}
            r = requests.post(endpoint,
                              headers={'Authorization': 'Bearer ' + result['access_token']}, json=email_msg)
            if r.ok:
                return {'result': 'ok'}
            else:

                return {'result': 'ko', 'error': r.json()}
        else:
            print(result.get("error"))
            print(result.get("error_description"))
            print(result.get("correlation_id"))