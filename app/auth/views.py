"""
modules used for auth/views.py
flask: framework used for project
flask_login: used to allow users to log in, log out, and gets the current_user
app.auth: used to get the auth blueprint for routes
app.models: used to get the User table to create and edit users
app.auth.forms: used to get the WTForms used throughout view functions
app: used to get db so we can perform SQLalchemy operations
app.send_email: used to send email to users when they register, confirm, and reset passwords
"""
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.auth import auth
from app.models import User
from app.auth.forms import LoginForm, RegistrationForm, ChangePasswordForm, PasswordResetRequestForm, PasswordResetForm
from app import db
from app.send_email import send_email


@auth.before_app_request
def before_request():
    """
    Function is a request hook that ensures the current_user passes all these criteria before
    confirming their account
    :return: redirects a user to a page telling them they have an unconfirmed account
    """
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint[:5] != 'auth.' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    """
    Function checks if a user is anonymous or using a confirmed account
    :return: if user passes if statement go to the main page, otherwise prompt the user that they are unconfirmed
    """
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Function allows users to login to their account
    Uses LoginForm for users to enter in their credentials
    Does a query on the database to see if they account is a valid account or not
    :return: redirects user to home page if they credentials match or prompts them with invalid and returns
    to login.html
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash('You have been logged in.')
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    """
    Function allows users to logout of their accounts
    :return: redirects user to main page after being logged out
    """
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Function allows users to create new accounts to login with
    Uses RegistrationForm for user to fill out their information
    An email is sent to the user after they submit to confirm their account
    :return: if the form was submitted successfully user is redirected to log in page,
    otherwise they are prompted with their registration errors
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(password=form.password.data, first_name=form.first_name.data, last_name=form.first_name.data,
                    email=form.email.data, phone=form.phone.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
                   'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    """
    Function used to confirm user accounts
    The link from a user's confirmation email must match token inorder for them to be confirmed
    :param token: token is the unique generated token that was created on account creation
    users confirmation must match this token
    :return: returns to main page with a prompt on whether or not they successfully confirmed their account or not
    """
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    """
    Function creates a new token for the user's account if they did not received the email or the token expired
    Sends a new confirmation email to the user's email address
    :return: redirects user back the main page afterwards
    """
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """
    Functinon used to change a user's password using the ChangePasswordForm
    :return: returns a html template for the form or main page if successfully completed
    """
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('Your password has been updated.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    return render_template("auth/change_password.html", form=form)


@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    """
    Function used to request a password reset
    first check that the current_user is not anonymous then check if the their email is in the database
    then prompt them that a email to reset their password has been sent
    :return:
    """
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset Your Password',
                       'auth/email/reset_password',
                       user=user, token=token,
                       next=request.args.get('next'))
        flash('An email with instructions to reset your password has been '
              'sent to you.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    """
    Function used to let users fill out the PasswordResetForm to reset their password if their token matches
    :param token: randomly generated token that the user must match in order to reset their password
    :return: returns a html template for main page or login page on successful password change
    """
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('main.index'))
        if user.reset_password(token, form.password.data):
            flash('Your password has been updated.')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)

