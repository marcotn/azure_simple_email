# azure_simple_email
Python library to send email trough azure service api

This tool is very simple to use provided you already have an active account with Microsoft Azure Cloud.

To ba able to access Azure Api this library will look for 3 environment variables 

AZURE_EMAIL_CLIENT_ID
AZURE_EMAIL_CLIENT_SECRET
AZURE_EMAIL_AUTHORITY

You can find these values inside your Azure Entra DI services,

Moreover to send an email you need to have a valid Microsoft email account inside the organization 

The you call instantiate AzureSendEmail passing the sender's email as paramenter

this is the example that I have tested here of course with different email address.

`azure_email = AzureSendMail(user_id='service@example.com')
azure_email.add_recipient('marco@test.com')
azure_email.add_attachment('../README.md')
azure_email.send_email(subject='test message', text='Hi, we are testing this python tool')
`
