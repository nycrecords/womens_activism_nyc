from flask_mail import Message
from app import mail
from threading import Thread

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    mail.send(msg)
    msg.html = html_body
    thr = Thread(target=send_async_email, args=(app, msg))
    thr.start()
