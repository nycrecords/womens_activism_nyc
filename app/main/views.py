from flask import Flask, render_template, request, flash
from .forms import FeedbackForm
from flask import current_app
from app.email import send_email
from ..models import Feedback
from . import main
# from ..import db
# from forms import Feedbackform
# from flask_mail import Mail, Message
# from ..email_notification import send_email


# main = Flask(__name__)

@main.route('/', methods=['GET','POST'])
def index():
    form = FeedbackForm()
    return render_template('index.html', form=form)

@main.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm()
# replace user with feedback
    if form.validate_on_submit():
        if 'tag' in form:
            tag_id = form.tag.data
        feedback = Feedback(email=form.email.data.lower(),
                title=form.subject.data,
                reason=form.reason.data)
        current_app.logger.info("Subject: {}\nEmail: {}\nReason: {}\n".format(form.subject.data, form.email.data, form.subject.data))

        send_email(feedback.email,
                   'Subject', 'index.html',
                   # reason=feedback.reason,
                   # title=feedback.title
                   )
    else:
        print(1)
        return render_template('index.html', form=form)
# feedback=feedback,
# subject=subject,
# reason=reason)

# msg = Message('WomensActivism.NYC Feedback Form', recipients=['sgong@records.nyc.gov'],
# sender='sgong@records.nyc.gov')
# msg.body = "Subject: {}\nEmail: {}\nReason: {}\n".format(form.subject.data, form.email.data, form.subject.data)
# mail.send(msg)

# current_app.logger.info('Sent login instructions to {}'.format(feedback.email))
# flash('User successfully registered\nAn email with login instructions has been sent to {}'.format(feedback.email),
# category='success')

# current_app.logger.info('End function admin_register() [VIEW]')
# return redirect(url_for('main.index'))

# current_app.logger.info('End function admin_register() [VIEW]')
# return render_template('auth/admin_register.html', form=form)


