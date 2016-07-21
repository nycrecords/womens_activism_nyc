from threading import Thread
from flask import current_app, render_template
from flask.ext.mail import Message
from . import mail


def send_async_email(current_app, msg):
    # TODO: Add comments
    with current_app.current_app_context():
        mail.send(msg)


def send_email(subject, template):
    # TODO: Add comments
    app = current_app._get_current_object()
    msg = Message(current_app.config['WomensActivism.NYC Feedback Form'] + ' ' + subject,
                  sender=app.config['sgong@records.nyc.gov'], recipients=['sgong@records.nyc.gov'])
    msg.html = render_template(template + '.html')
    thr = Thread(target=send_async_email, args=[current_app, msg])
    thr.start()
    return thr
