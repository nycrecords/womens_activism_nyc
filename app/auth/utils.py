'''
Utility functions used for view functions involving login
'''

from app.models import Users

def create_login_log(form_email, login_validation):
    '''
    A utility function to log login success and failure in Events table
    :param form.data
    '''
    user = Users.query.filter_by(email=form_email).first()
