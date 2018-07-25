"""
WTForms used for Featured Stories
"""
from flask_wtf import FlaskForm
from wtforms import (
    SubmitField,
    TextAreaField,
    RadioField,
    StringField,
    SelectField
)
from wtforms.validators import (
    DataRequired,
    Length
)


class FeaturedStoryForm(FlaskForm):
    """
    The WTForm used to create a new featured story
    """
    left_right = RadioField("Picture on Left or Right", choices=[('left', "Picture on Left Side"), ('right', "Picture on Right Side")],
                            validators=[DataRequired()], default='left')
    title = StringField("Title/Position", validators=[DataRequired()])
    description = TextAreaField("Insert a text here", validators=[DataRequired(), Length(max=395)])
    rank_choices = [(str(n+1), str(n+1)) for n in range(5)]
    rank = SelectField("Rank", choices=[], default=0, coerce=int)
    submit = SubmitField('Submit')


class ModifyFeatureForm(FlaskForm):
    """
    The WTForm used to create a new featured story
    """
    left_right = RadioField("Picture on Left or Right", choices=[('True', "Picture on Left Side"),
                                                                 ('False', "Picture on Right Side")],
                            validators=[DataRequired()], default='left')

    title = StringField("Title/Position", validators=[DataRequired()])

    description = TextAreaField("Insert a text here", validators=[DataRequired(), Length(max=395)])

    is_visible = RadioField("Visibility", choices=[('True', "Visible"), ('False', "Not Visible")],
                            validators=[DataRequired()], default='True')

    rank = SelectField("Rank", choices=[], default=0, coerce=int)

    submit = SubmitField('Submit')


