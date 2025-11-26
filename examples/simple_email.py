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



#content_file = open("birthday.html", 'r')
#_content = content_file.read()
#res=azure_email.send_mail_mime_types(subject='test message', content=_content)
#print(res)
#content_file.close()

#test with ccn

azure_email = AzureSendMail(user_id=TEST_SENDER)
azure_email.sender = OVERRIDE_TEST_SENDER
azure_email.add_recipient(TEST_RECIPIENT)
azure_email.add_cc_recipient(TEST_CC_RECIPIENT)
azure_email.add_ccn_recipient(TEST_CCN_RECIPIENT)
azure_email.add_attachment('../README.md')
res = azure_email.send_email(subject='test message', text='Hi, we are testing <h3>this</h3> python tool',
                             content_type='html')
print(res)

print(os.getcwd())
_html_content = open("html/test_email.html", "r").read()
res_mime = azure_email.send_mail_mime_types(subject='test message', content=_html_content)
print(res_mime)

#test with reply to

azure_email = AzureSendMail(user_id=TEST_SENDER)
azure_email.sender = OVERRIDE_TEST_SENDER
azure_email.add_recipient(TEST_RECIPIENT)
azure_email.add_cc_recipient(TEST_CC_RECIPIENT)
azure_email.add_ccn_recipient(TEST_CCN_RECIPIENT)
azure_email.add_reply_to(TEST_REPLY_TO)
azure_email.add_attachment('../README.md')
res = azure_email.send_email(subject='test message', text='Hi, we are testing <h3>this</h3> python tool',
                             content_type='html')
print(res)

