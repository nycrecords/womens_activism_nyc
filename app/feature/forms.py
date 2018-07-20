"""
WTForms used for Featured Stories
"""
from flask_wtf import FlaskForm
from wtforms import (
    SubmitField,
    TextAreaField,
    RadioField,
    StringField
)
from wtforms.validators import (
    DataRequired
)


class FeaturedStoryForm(FlaskForm):
    """
    The WTForm used to create a new featured story
    """
    left_right = RadioField("Picture on Left or Right", choices=[('left', "Picture on Left Side"), ('right', "Picture on Right Side")],
                            validators=[DataRequired()], default='left')
    title = StringField("Title/Position", validators=[DataRequired()])
    quote = TextAreaField("Insert a quote here", validators=[DataRequired()])
    submit = SubmitField('Submit')


class ModifyFeatureForm(FlaskForm):
    """
    The WTForm used to create a new featured story
    """
    left_right = RadioField("Picture on Left or Right", choices=[('True', "Picture on Left Side"),
                                                                 ('False', "Picture on Right Side")],
                            validators=[DataRequired()], default='left')

    title = StringField("Title/Position", validators=[DataRequired()])

    quote = TextAreaField("Insert a quote here", validators=[DataRequired()])

    is_visible = RadioField("Visibility", choices=[('True', "Visible"), ('False', "Not Visible")],
                            validators=[DataRequired()], default='True')

    submit = SubmitField('Submit')
