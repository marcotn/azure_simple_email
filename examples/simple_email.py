from azure_simple_email.azure_mail import AzureSendMail

#MY_TEST_EMAIL=test@azure-customer.it

azure_email = AzureSendMail(user_id='test@test.com')
azure_email.add_recipient('someone@test.com')
azure_email.add_attachment('../README.md')
azure_email.send_email(subject='test message', text='Hi, we are testing this python tool')

