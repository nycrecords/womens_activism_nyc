from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from app.models import Users
from .forms import LoginForm
from app.auth.utils import create_login_log

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data, is_admin=True).one_or_none()
        if user is not None and user.verify_password(form.password.data) and user.is_admin:
            login_user(user)
            create_login_log(user, True)
            return redirect(request.args.get('next') or url_for('main.index'))

        flash('Invalid username or password.')
        create_login_log(user, False)

    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('main.index'))