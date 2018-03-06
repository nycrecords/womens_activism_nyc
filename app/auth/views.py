from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from app.models import Users
from .forms import LoginForm
from app.auth.utils import create_login_log

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    A view function that determines whether if the attempt is successful or not
    :param login email and password
    :return (success: main.index , fail: auth/login)

    scenario 1. if user is already authenticated, then redirect the user to the main page
    scenario 2. if user that provided the email and password matches the record in the database, we check if they are an admin
                    we log the user
                    create an audit trail (login success)
                    redirect user to main page
               else (validated)
                    create an audit trail (login fail) with the attempted email recorded
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data, is_admin=True).one_or_none()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            create_login_log(user, login_validation=True)
            return redirect(request.args.get('next') or url_for('main.index'))

        flash('Invalid username or password.')
        create_login_log(user, login_validation=False, emailAttempted=form.email.data)

    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('main.index'))