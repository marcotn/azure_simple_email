import mimetypes
import os
from azure_simple_email.azure_mail import AzureSendMail

TEST_SENDER = os.environ.get('TEST_SENDER', 'service@example.com')
TEST_RECIPIENT = os.environ.get('TEST_RECIPIENT', 'marco@test.com')

azure_email = AzureSendMail(user_id=TEST_SENDER)
azure_email.add_recipient(TEST_RECIPIENT)
azure_email.add_attachment('../README.md')
azure_email.send_email(subject='test message', text='Hi, we are testing this python tool')

content_file = open("birthday.html", 'r')
_content = content_file.read()
res=azure_email.send_mail_mime_types(subject='test message', content=_content)
print(res)

