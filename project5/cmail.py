import smtplib
from email.message import EmailMessage
def send_email(subject, body, to):
    server=smtplib.SMTP_SSL('smtp.gmail.com',465)

    server.login('your_email@gmail.com', 'your_password')
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = 'your_email@gmail.com'
    msg['To'] = to
    msg.set_content(body)
    server.send_message(msg)
    print('mail sent')
    server.close()