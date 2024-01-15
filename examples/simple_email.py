from azure_simple_email.azure_mail import AzureSendMail


azure_email = AzureSendMail(user_id='service@example.com')
azure_email.add_recipient('marco@test.com')
azure_email.add_attachment('../README.md')
azure_email.send_email(subject='test message', text='Hi, we are testing this python tool')


