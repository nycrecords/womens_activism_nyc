from flask import current_app
from flask_mail import Message
from app import mail
from threading import Thread



def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.html = html_body
    mail.send(msg)
    thr = Thread(target=send_async_email, args=(current_app, msg))
    thr.start()
