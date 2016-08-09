"""
Modules used for auth/forms.py
flask_wtf: wrapper class for WTForms
WTForms: used to create web forms for Users
WTForms.validators: used to validate the fields in the
app.models: import User table from models.py
"""
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo
from app.models import User


class LoginForm(Form):
    """
    WTForm used for users to login to their accounts
    users log in with their email and have an option to stay logged in with remember_me
    """
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(Form):
    """
    WTForm used for new users to register accounts
    the data from this form will be passed in to create a User object from models
    """

    first_name = StringField('First Name', validators=[DataRequired(), Length(1,30)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(1, 30)])
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    phone = StringField('Phone (no spaces or dashes)', validators=[DataRequired(), Length(1,10)])
    password = PasswordField('Password (must be at lease 8 characters long with one capital and one number)',
                             validators=[DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')


    def validate_email(self, field):
        """
        function used to check if the email the user is using is already registered in the database

        :param field: the email field from the RegistrationForm
        :return: A validation message if the email is already registered in the database
        """
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_password(self, password_field):
        """
        Used to verify that password meets security criteria.

        :param password_field: password field
        :return: A validation message if password is not secure.
        """
        if len(password_field.data) < 8:
            raise ValidationError('Your password must be 8 or more characters')

        has_num = False
        has_capital = False
        for i in password_field.data:
            if i.isdigit():
                has_num = True
            if i.isupper():
                has_capital = True

        if not (has_num or has_capital):
            raise ValidationError('Passwords must contain at least one number and one capital letter')

        if not has_num:
            raise ValidationError('Password must contain at least one number')

        if not has_capital:
            raise ValidationError('Password must contain at least one capital letter')


class ChangePasswordForm(Form):
    """
    WTForm used for users to change their existing password, only visible when a user is logged in
    Users enter their old password and the new password they want to change it to
    """
    old_password = PasswordField('Old password', validators=[DataRequired()])
    password = PasswordField('New password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm new password', validators=[DataRequired()])
    submit = SubmitField('Update Password')


class PasswordResetRequestForm(Form):
    """
    WTForm used for a user to request a password reset
    an email will be sent to the user if their email is valid
    """
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    submit = SubmitField('Reset Password')


class PasswordResetForm(Form):
    """
    WTForm used to reset their password
    user will enter their email to verify their account and then their newly selected password
    """
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('New Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unknown email address.')
