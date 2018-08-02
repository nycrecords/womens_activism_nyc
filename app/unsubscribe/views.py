from flask import render_template, flash, request, Markup

from app.unsubscribe import unsubscribe
from app.unsubscribe.forms import UnsubscribeForm
from app.models import Flags
from app.constants.flags import UNSUBSCRIBED
from app.db_utils import create_object

@unsubscribe.route('/', methods=['GET', 'POST'])
def unsubscribe():
    form = UnsubscribeForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            if form.email.data:
                flash(Markup('You are no longer subscribed.'), category='success')
                flag = Flags(type=UNSUBSCRIBED,
                             reason=reason)
                create_object(flag)
                return render_template('unsubscribe/unsubscribe.html', form=form)
    return render_template('unsubscribe/unsubscribe.html', form=form)
