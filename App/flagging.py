from flask import Flask, render_template, session, redirect, url_for, flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import Form
from wtforms import SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_mail import Message

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['WOMENS_ACTIVISM_NYC_PREFIX'] = '[WomensActivismNYC]'
app.config['WOMENS_ACTIVISM_NYC_MAIL_SENDER'] = 'Flagging Bot <jmo@records.nyc.gov>'

def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['WOMENS_ACTIVISM_NYC_PREFIX'] + subject,
                  sender=app.config['WOMENS_ACTIVISM_NYC_MAIL_SENDER'], recipients=[to])
    msg.body = render_tempplate(template + '.txt', **kwargs)

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

flag_choices = [('inappropriate', 'Inappropriate content'), ('offensive', "Offensive content"), ('incorrect', 'Incorrect information'), ('other', 'Other')]
post_title = 'The Life of Harriet Tubman'


class FlaggingForm(Form):
    flag_reason = SelectField('Reason for flagging?', choices=flag_choices, validators=[DataRequired('Please Select a reason')])
    flag_description = TextAreaField('Please provide a brief description', validators=[Length(0, 500)])
    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    form = FlaggingForm()
    # On final build there should be a variable "post_title" gotten from calling DB/URL/etc
    if form.validate_on_submit():
        flash('Thanks for your input')
        flag_reason = form.flag_reason.data
        flag_description = form.flag_description.data
        print('Flag_reason: {}\nFlag_description: {}'.format(flag_reason, flag_description))
        session['flag_reason'] = form.flag_reason.data
        return redirect(url_for('index'))
    return render_template('flagging.html', form=form, post_title=post_title)

if __name__ == '__main__':
    manager.run()




