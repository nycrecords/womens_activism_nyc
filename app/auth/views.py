"""
modules used for auth/views.py
flask: framework used for project
flask_login: used to allow users to log in, log out, and gets the current_user
app.auth: used to get the auth blueprint for routes
app.models: used to get the User table to create and edit users
app.auth.forms: used to get the WTForms used throughout view functions
app: used to get db so we can perform SQLalchemy operations
app.send_email: used to send email to users when they register, confirm, and reset passwords
app.db_helpers: used as utility functions for SQLalchemy operations
"""
from flask import render_template, redirect, request, url_for, flash, current_app, session
from flask_login import login_user, logout_user, login_required, current_user
from app.auth import auth
from app.models import User
from app.auth.forms import LoginForm, RegistrationForm, ChangePasswordForm, PasswordResetRequestForm, PasswordResetForm
from app.send_email import send_email
from app.db_helpers import put_obj
from datetime import datetime
from werkzeug.security import check_password_hash
from .modules import check_password_requirements
from app.utils import InvalidResetToken
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


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


# @auth.route('/login', methods=['GET', 'POST'])
# def login():
#     """
#     Function allows users to login to their account
#     Uses LoginForm for users to enter in their credentials
#     Does a query on the database to see if they account is a valid account or not
#     :return: redirects user to home page if they credentials match or prompts them with invalid and returns
#     to login.html
#     """
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data.lower()).first()
#         if user is not None and user.verify_password(form.password.data):
#             login_user(user, form.remember_me.data)
#             flash('You have been logged in.')
#             return redirect(request.args.get('next') or url_for('main.index'))
#         flash('Invalid username or password.')
#     return render_template('auth/login.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    View function to login a user. Redirects the user to the index page on successful login.

    :return: Login page.
    """
    current_app.logger.info('Start function login() [VIEW]')
    # Redirect to index if already logged in
    if current_user.is_authenticated:
        current_app.logger.info('{} is already authenticated: redirecting to index'.format(current_user.email))
        current_app.logger.info('End function login() [VIEW]')
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=(form.email.data).lower()).first()

        if user and user.login_attempts >= 2:
            # Too many invalid attempts
            current_app.logger.info('{} has been locked out'.format(user.email))
            flash('You have too many invalid login attempts. You must reset your password.',
                  category='error')
            current_app.logger.info('End function login() [VIEW]')
            return redirect(url_for('auth.password_reset_request'))

        if user is not None and user.verify_password(form.password.data):
            # Credentials successfully submitted
            login_user(user)
            user.login_attempts = 0
            # db.session.add(user)
            # db.session.commit()
            put_obj(user)
            current_app.logger.info('{} successfully logged in'.format(current_user.email))
            #flash('You have been logged in')
            #return redirect(url_for('main.index'))

            # Check to ensure password isn't outdated
            if (datetime.today() - current_user.password_list.last_changed).days > 90:
                # If user's password has expired (not update in 90 days)
                current_app.logger.info('{}\'s password hasn\'t been updated in 90 days: account invalidated.'
                                        .format(current_user.email))
                current_user.confirmed = False
                # db.session.add(current_user)
                # db.session.commit()
                put_obj(current_user)
                flash('You haven\'t changed your password in 90 days. You must re-validate your account',
                      category='error')
                current_app.logger.info('End function login() [VIEW]')
                return redirect(url_for('auth.change_password'))

            if (datetime.today() - current_user.password_list.last_changed).days > 75:
                # If user's password is about to expire (not updated in 75 days)
                days_to_expire = (datetime.today() - current_user.password_list.last_changed).days
                flash('Your password will expire in {} days.'.format(days_to_expire), category='warning')
            current_app.logger.error('{} is already logged in. Redirecting to main.index'.format(current_user.email))
            current_app.logger.info('End function login() [VIEW]')
            flash('You have been logged in.')
            return redirect(request.args.get('next') or url_for('main.index'))

        if user:
            current_app.logger.info('{} failed to log in: Invalid username or password'.format(user.email))
            user.login_attempts += 1
            # db.session.add(user)
            # db.session.commit()
            put_obj(user)
        flash('Invalid username or password', category='error')
    current_app.logger.info('End function login() [VIEW]')
    return render_template('auth/login.html', form=form, reset_url=url_for('auth.password_reset_request'))


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
    current_app.logger.info('Start function register() [VIEW]')
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(password=form.password.data, first_name=form.first_name.data, last_name=form.last_name.data,
                    email=form.email.data, phone=form.phone.data)
        put_obj(user)
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
                    'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        current_app.logger.info('End function register() [VIEW]')
        return redirect(url_for('auth.login'))
    current_app.logger.info('End function register() [VIEW]')
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
    # """
    # Functinon used to change a user's password using the ChangePasswordForm
    # :return: returns a html template for the form or main page if successfully completed
    # """
    # form = ChangePasswordForm()
    # if form.validate_on_submit():
    #     if current_user.verify_password(form.old_password.data):
    #         current_user.password = form.password.data
    #         put_obj(current_user)
    #         flash('Your password has been updated.')
    #         return redirect(url_for('main.index'))
    #     else:
    #         flash('Invalid password.')
    # return render_template("auth/change_password.html", form=form)

    current_app.logger.info('Start function change_password() [VIEW]')
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if (
                                check_password_hash(pwhash=current_user.password_list.p1,
                                                    password=form.password.data) or
                                check_password_hash(pwhash=current_user.password_list.p2,
                                                    password=form.password.data) or
                            check_password_hash(pwhash=current_user.password_list.p3,
                                                password=form.password.data) or
                        check_password_hash(pwhash=current_user.password_list.p4,
                                            password=form.password.data) or
                    check_password_hash(pwhash=current_user.password_list.p5,
                                        password=form.password.data)
        ):
            # If the inputted password is one of the user's last five passwords
            current_app.logger.info('{} tried to change password. Failed: Used old password.'.format(
                current_user.email))
            flash('Your password cannot be the same as the last 5 passwords', category='error')
            return render_template("auth/change_password.html", form=form)

        elif check_password_requirements(
                current_user.email,
                form.old_password.data,
                form.password.data,
                form.password2.data):
            # If password security requirements are met
            current_user.password_list.update(current_user.password_hash)
            current_user.password = form.password.data
            current_user.validated = True
            # db.session.add(current_user)
            # db.session.commit()
            put_obj(current_user)
            current_app.logger.info('{} changed their password.'.format(current_user.email))
            flash('Your password has been updated.', category='success')
            current_app.logger.info('End function logout() [VIEW]')
            return redirect(url_for('main.index'))

    current_app.logger.info('End function logout() [VIEW]')
    return render_template("auth/change_password.html", form=form)


@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    # """
    # Function used to request a password reset
    # first check that the current_user is not anonymous then check if the their email is in the database
    # then prompt them that a email to reset their password has been sent
    # :return:
    # """
    # if not current_user.is_anonymous:
    #     return redirect(url_for('main.index'))
    # form = PasswordResetRequestForm()
    # if form.validate_on_submit():
    #     user = User.query.filter_by(email=form.email.data).first()
    #     if user:
    #         token = user.generate_reset_token()
    #         send_email(user.email, 'Reset Your Password',
    #                    'auth/email/reset_password',
    #                    user=user, token=token,
    #                    next=request.args.get('next'))
    #     flash('An email with instructions to reset your password has been '
    #           'sent to you.')
    #     return redirect(url_for('auth.login'))
    # return render_template('auth/reset_password.html', form=form)

    """
    View function for requesting a password reset.

    :return: HTML page in which users can request a password reset.
    """
    current_app.logger.info('Start function password_reset_request() [VIEW]')
    if not current_user.is_anonymous:
        current_app.logger.info('Current user ({}) is already signed in. Redirecting to index...'.
                                format(current_user.email))
        return redirect(url_for('main.index'))

    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        current_app.logger.info('Tried to submit a password reset request with account email {}'.format(
            form.email.data))
        current_app.logger.info('Querying for user with given email: {}'.format(form.email.data))
        user = User.query.filter_by(email=(form.email.data).lower()).first()
        current_app.logger.info('Finished querying for user with given email')
        if user:
            token = user.generate_reset_token()
            send_email(user.email,
                       'Reset Your Password',
                       'auth/email/reset_password',
                       user=user,
                       token=token,
                       next=request.args.get('next'))
            current_app.logger.info('Sent password reset instructions to {}'.format(form.email.data))
            flash('An email with instructions to reset your password has been sent to you.', category='success')
        else:
            current_app.logger.info('Requested password reset for e-mail %s but no such account exists' %
                                    form.email.data)
            flash('An account with this email was not found in the system.', category='error')
        current_app.logger.info('Redirecting to /auth/login...')
        current_app.logger.info('End function password_reset_request() [VIEW]')
        return redirect(url_for('auth.login'))
    current_app.logger.info('End function password_reset_request() [VIEW]')
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
            user.password=form.password.data
            put_obj(user)
            flash('Your password has been updated.')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)

    # """
    #     View function after a user has clicked on a password reset link in their inbox.
    #
    #     :param token: The token that is checked to verify the user's credentials.
    #     :return: HTML page in which users can reset their passwords.
    #     """
    # current_app.logger.info('Start function password_reset [VIEW]')
    # if not current_user.is_anonymous:
    #     # If a user is signed in already, redirect them to index
    #     current_app.logger.info('{} is already signed in. redirecting to /index...'.format(current_user.email))
    #     current_app.logger.info('End function password_reset')
    #     return redirect(url_for('main.index'))
    #
    # form = PasswordResetForm()
    # if form.validate_on_submit():
    #     s = Serializer(current_app.config['SECRET_KEY'])
    #     try:
    #         data = s.loads(token)
    #     except:
    #         # Token has timed out
    #         current_app.logger.error('EXCEPTION (ValueError): Token no longer valid')
    #         flash('This token is no longer valid.', category='warning')
    #         current_app.logger.info('End function password_reset')
    #         return redirect(url_for('auth.login'))
    #
    #     current_app.logger.error('Querying for user that corresponds to given token')
    #     user = User.query.filter_by(id=data.get('reset')).first()
    #     current_app.logger.error('Finished querying for user')
    #
    #     if user is None:
    #         # If the user associated with the token does not exist, log an error and redirect user to index
    #         current_app.logger.error('Requested password reset for invalid account.')
    #         current_app.logger.info('End function password_reset')
    #         return redirect(url_for('main.index'))
    #
    #     elif (
    #                             check_password_hash(pwhash=user.password_list.p1,
    #                                                 password=form.password.data) or
    #                             check_password_hash(pwhash=user.password_list.p2,
    #                                                 password=form.password.data) or
    #                         check_password_hash(pwhash=user.password_list.p3,
    #                                             password=form.password.data) or
    #                     check_password_hash(pwhash=user.password_list.p4,
    #                                         password=form.password.data) or
    #                 check_password_hash(pwhash=user.password_list.p5,
    #                                     password=form.password.data)
    #     ):
    #         # If user tries to set password to one of last five passwords, flash an error and reset the form
    #         current_app.logger.error('{} tried to change password. Failed: Used old password.'.format(
    #             user.email))
    #         flash('Your password cannot be the same as the last 5 passwords', category='error')
    #         current_app.logger.info('End function password_reset')
    #         return render_template("auth/reset_password.html", form=form)
    #     else:
    #         try:
    #             if 'reset_token' in session and session['reset_token']['valid'] and user.reset_password(token,form.password.data):
    #                 # If the token has not been used and the user submits a proper new password, reset users password
    #                 # and login attempts
    #                 user.login_attempts = 0
    #                 # db.session.add(user)
    #                 # db.session.commit()
    #                 put_obj(user)
    #                 session['reset_token']['valid'] = False  # Now that the token has been used, invalidate it
    #                 current_app.logger.error('Successfully changed password for {}'.format(user.email))
    #                 flash('Your password has been updated.', category='success')
    #                 current_app.logger.info('End function password_reset... redirecting to login')
    #                 return redirect(url_for('auth.login'))
    #
    #             elif 'reset_token' in session and not session['reset_token']['valid']:
    #                 # If the token has already been used, flash an error message
    #                 current_app.logger.error('Failed to change password for {}: token invalid (already used)'
    #                                          .format(user.email))
    #                 flash('You can only use a reset token once. Please generate a new reset token.', category='error')
    #                 current_app.logger.info('End function password_reset')
    #                 return render_template('auth/reset_password.html', form=form)
    #
    #             else:
    #                 # New password didn't meet minimum security criteria
    #                 current_app.logger.error(
    #                     'Entered invalid new password for {}'.format(user.email))
    #                 flash('Password must be at least 8 characters with at least 1 Uppercase Letter and 1 Number',
    #                       category='error')
    #                 current_app.logger.info('End function password_reset')
    #                 return render_template('auth/reset_password.html', form=form)
    #
    #         except InvalidResetToken:
    #             current_app.logger.error('EXCEPTION (InvalidResetToken): Token no longer valid')
    #             flash('This token is no longer valid.', category='warning')
    #             current_app.logger.info('End function password_reset')
    #             return login()
    #
    # current_app.logger.info('End function password_reset')
    # return render_template('auth/reset_password.html', form=form)

