from flask  import render_template, redirect, url_for, current_app, flash
from .. import db
from ..models import *
from ..email import send_email
from . import flags
from .forms import FlagsForm


@flags.route('/flags', methods=['GET', 'POST'])
def flags():
    form = FlagsForm()
    # On final build there should be a variable "post_title" gotten from calling DB/URL/etc
    if form.validate_on_submit():
        flash('Thanks for your input, a moderator has been notified')
        flags = Flag(type=form.flag_reason.data,
                     reason=form.flag_description.data)
        current_app.logger.info(
            "Flag_reason: {}\nFlag_description: {}".format(form.flag_reason.data, form.flag_description.data))
        send_email(to=current_app.config['FLAG_MAIL_ADMIN'], subject='Flag', template='email_flags',
                   reason=flags.type, description=flags.reason)
        return redirect(url_for('main.flags'))
    else:
        return render_template('flags.html', form=form, post_title=post_title)