import base64
import mimetypes
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
import msal
import requests


logger = logging.getLogger(__name__)

class AzureSendMail:

    def __init__(self, user_id):
        self.to = []
        self.reply_to = []
        self.cc = []
        self.bcc = []
        self.attachments = []
        self.user_id = user_id
        self.sender = user_id
        #self.endpoint = f'https://graph.microsoft.com/v1.0/users/{self.sender}/sendMail'
        self.DEBUG_MODE = os.environ.get("DEBUG_MODE", None) != None
        self.DEBUG_EMAIL = os.environ.get("DEBUG_EMAIL", 'marco.pavanelli@sasabz.it')
        self.token = None

    def get_endpoint(self):
        return f'https://graph.microsoft.com/v1.0/users/{self.sender}/sendMail'

    def add_recipient(self, recipient: str):
        self.to.append(recipient)

    def add_cc_recipient(self, recipient: str):
        self.cc.append(recipient)

    def add_ccn_recipient(self, recipient: str):
        self.bcc.append(recipient)

    def add_reply_to(self, reply_to: str):
        self.reply_to.append(reply_to)

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

    def create_message(self, subject, content):

        message = MIMEMultipart("alternative")
        _html = MIMEText(content, "html")
        message.attach(_html)
        if self.DEBUG_MODE:
            message['to'] = self.DEBUG_EMAIL
            debug_text = (f"to: {self.to[0]} \ncc: {self.cc} \nbcc: {self.bcc} \n from: {self.sender}"
                          f"subject: {subject}")
            debug_text = MIMEText(debug_text, "plain")
            message.attach(debug_text)
        else:
            message['to'] = self.to[0]
            message['cc'] = ','.join(self.cc)
            message['bcc'] = ','.join(self.bcc)
            message['reply-to'] = ','.join(self.reply_to)
            message['from'] = self.sender
            message['subject'] = subject
        raw = base64.b64encode(message.as_bytes())
        #raw = base64.urlsafe_b64encode(message.as_bytes())
        return raw.decode()


    def send_mail_mime_types(self, subject: str, content: str):
        if not self.token:
            self.token = self.get_token()
        if "access_token" in self.token:
            email_msg = self.create_message(subject=subject, content=content)
            headers = {'Authorization': 'Bearer ' + self.token['access_token']}
            headers['Content-Type'] = 'text/plain'
            if os.environ.get('DEBUG_DO_NOT_SEND', '0') == '1':
                logger.info(email_msg)
            else:
                r = requests.post(self.get_endpoint(),
                              headers=headers, data=email_msg)
                if r.ok:
                    return {'result': 'ok'}
                else:
                    return {'result': 'ko', 'error': r.json()}
        else:
            print(self.token("error"))
            print(self.token.get("error_description"))
            print(self.token.get("correlation_id"))


    def send_email(self, subject: str, text: str, content_type='Text'):
        """Sends Out The actual email
           Parameters:
           subject string
           test string
           content_type string (either "text" ot "html")
        """
        if not self.token:
            self.token = self.get_token()
        replyTo= [{'EmailAddress': {'Address': _email}} for _email in self.reply_to]
        toRecipients= [{'EmailAddress': {'Address': _email}} for _email in self.to]
        ccRecipients= [{'EmailAddress': {'Address': _email}} for _email in self.cc]
        bccRecipients= [{'EmailAddress': {'Address': _email}} for _email in self.bcc]
        if "access_token" in self.token:
            if self.DEBUG_MODE:
                body_debug = f"to: {toRecipients} \n cc: {ccRecipients} \n bcc: {bccRecipients}"
                body_text = f"{body_debug} \n\n {text}"
                email_msg = {'Message': {'Subject': subject,
                                         'Body': {'ContentType': content_type, 'Content': body_text},
                                         'From': {'EmailAddress': {'Address': self.sender}},
                                         'toRecipients': [{'EmailAddress': {'Address': self.DEBUG_EMAIL}}],
                                         'replyTo': replyTo,
                                         'Attachments': self.attachments
                                         },
                             'SaveToSentItems': 'true'}
            else:
                email_msg = {'Message': {'Subject': subject,
                                         'Body': {'ContentType': content_type, 'Content': text},
                                         'From': {'EmailAddress': {'Address': self.sender}},
                                         'toRecipients': toRecipients,
                                         'ccRecipients': ccRecipients,
                                         'bccRecipients': bccRecipients,
                                         'replyTo': replyTo,
                                         'Attachments': self.attachments
                                         },
                             'SaveToSentItems': 'true'}
            if os.environ.get('DEBUG_DO_NOT_SEND', '0') == '1':
                logger.info(email_msg)
                return {'result': 'ok'}
            else:
                r = requests.post(self.get_endpoint(), headers={'Authorization': 'Bearer ' + self.token['access_token']}, json=email_msg)
                if r.ok:
                    return {'result': 'ok'}
                else:
                    return {'result': 'ko', 'error': r.text}
        else:
            print(self.token.get("error"))
            print(self.token.get("error_description"))
            print(self.token.get("correlation_id"))


    def clear(self):
        self.to = []
        self.reply_to = []
        self.cc = []
        self.bcc = []
        self.attachments = []