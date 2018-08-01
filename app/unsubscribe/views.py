from flask import render_template, flash, request, Markup

from app.unsubscribe import unsubscribe
from app.unsubscribe.forms import UnsubscribeForm


@unsubscribe.route('/', methods=['GET', 'POST'])
def unsubscribe():
    form = UnsubscribeForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            if form.email.data :
                flash(Markup('You are no longer subscribed.'), category='success')
                return render_template('unsubscribe/unsubscribe.html', form=form)
    return render_template('unsubscribe/unsubscribe.html', form=form)
