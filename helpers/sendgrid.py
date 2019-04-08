import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def deliver_mail():
    message = Mail(
        from_email='admin@nextagram.com',
        to_emails='shannonsimoncherry@gmail.com',
        subject='Thank you for your donation.',
        html_content='<strong>Your donation was received! Thank you.</strong>')
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)

    except Exception as e:
        print(e.message)

    
# def deliver_email():
#     from_email = Email("admin@nextagram.com")
#     to_email = Email("shannonsimoncherry@gmail.com")
#     subject = "Thank you for your donation!"
#     content = Content("text/plain", "Your donation was received.")
#     mail = Mail(from_email, subject, to_email, content)
#     response = sg.client.mail.send.post(request_body=mail.get())
#     print(response.status_code)
#     print(response.body)
#     print(response.headers)