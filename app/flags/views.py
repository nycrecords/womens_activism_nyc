# TODO: Module level docstring
from flask  import render_template, redirect, url_for, current_app, flash
from .. import db
from ..models import Flag, Post
from ..send_email import send_email
from . import flags
from .forms import FlagsForm


@flags.route('/flag/<int:id>', methods=['GET', 'POST'])
def flags(id):
    # TODO: Function docstring
    post = Post.query.get_or_404(id)
    post_title = post.title
    print(post_title)

    form = FlagsForm()
    if form.validate_on_submit():
        flash('Thank you for your input, a moderator has been notified.')
        flags = Flag(post_id=post.id,
                    type=form.flag_reason.data,
                    reason=form.flag_description.data)
        # TODO: Should be done in a separate file (utils)
        db.session.add(flags)
        db.session.commit()
        current_app.logger.info(
            "Flag_reason: {}\nFlag_description: {}".format(form.flag_reason.data, form.flag_description.data))
        send_email(to=current_app.config['WOMENS_ADMIN'], subject='Flag', template='mail/email_flags',
                   post_title=post_title, reason=flags.type, description=flags.reason)
        return redirect(url_for('main.index'))
    return render_template('flags.html', form=form, post_title=post_title)
