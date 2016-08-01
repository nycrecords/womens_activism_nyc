from threading import Thread
from flask import current_app, render_template
from flask.ext.mail import Message
from . import mail


def send_async_email(current_app, msg):
    # TODO: Add comments
    with current_app.current_app_context():
        mail.send(msg)
