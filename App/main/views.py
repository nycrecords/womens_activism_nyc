from flask import render_template, redirect, url_for, current_app, flash
from .. import db
from ..models import *
from ..email import send_email
from . import main
from .forms import FeedbackForm, PostForm
from flask_login import login_required


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        post = Post(title=title, content=content, creation_time=db.func.current_timestamp(),
                    is_edited=False, is_visible=True)
        db.session.add(post)
        flash('Post submitted!')
        return redirect(url_for('.index'))
    posts = Post.query.order_by(Post.creation_time.desc()).all()
    return render_template('index.html',form=form, posts=posts)


@main.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm()

    if form.validate_on_submit():
        subject = form.subject.data
        email = form.email.data
        reason = form.reason.data
        print('Subject: {}\nEmail: {}\nReason: {}'.format(subject, email, reason))

        feedback = Feedback(title=subject, email=email, reason=reason)
        db.session.add(feedback)

        send_email(current_app.config['WOMENS_ADMIN'],'New Feedback', 'mail/new_user', feedback=feedback)

        flash('Thank you for your feedback!')
        return redirect(url_for('.feedback'))
    return render_template('feedback.html', form=form)


@main.route('/secret', methods=['GET', 'POST'])
@login_required
def secret():
    return render_template('secret.html')