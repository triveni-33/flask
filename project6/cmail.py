import smtplib
from email.message import EmailMessage
def send_mail(to,subject,body):
    server=smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.login('boyapatitriveni5@gmail.com','gqrc azfv adlu utgi')
    msg=EmailMessage()
    msg['FROM']='boyapatitriveni5@gmail.com'
    msg['TO']=to
    msg['SUBJECT']=subject
    msg.set_content(body)
    server.send_message(msg)
    print('Mail sent')
    server.close()


