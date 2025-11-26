import os
from azure_simple_email.azure_mail import AzureSendMail

TEST_SENDER = os.environ.get('TEST_SENDER', 'service@example.com')
TEST_RECIPIENT = os.environ.get('TEST_RECIPIENT', 'marco@test.com')
TEST_CC_RECIPIENT = os.environ.get('TEST_CC_RECIPIENT', 'marco@test.com')
TEST_CCN_RECIPIENT = os.environ.get('TEST_BCC_RECIPIENT', 'marco@test.com')
OVERRIDE_TEST_SENDER = os.environ.get('OVERRIDE_TEST_SENDER', 'marco.pavanelli@sasabz.it')
TEST_REPLY_TO = os.environ.get('TEST_REPLY_TO', 'marco.pavanelli@gmail.com')

azure_email = AzureSendMail(user_id=TEST_SENDER)
azure_email.sender = OVERRIDE_TEST_SENDER
azure_email.add_recipient(TEST_RECIPIENT)
azure_email.add_attachment('../README.md')
azure_email.reply_to = [OVERRIDE_TEST_SENDER]
azure_email.send_email(subject='test message', text='Hi, we are testing <h1>this<h1> python tool')

#try to send multiple times with the same token
azure_email.sender = OVERRIDE_TEST_SENDER
azure_email.add_recipient(TEST_CC_RECIPIENT)
azure_email.add_attachment('../README.md')
azure_email.reply_to = [OVERRIDE_TEST_SENDER]
azure_email.send_email(subject='Second send without obtaining test message', text='Hi, we are testing <h1>this<h1> python tool')
