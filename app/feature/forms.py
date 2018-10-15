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
    left_right = RadioField("Picture on Left or Right", choices=[('left', "Picture on Left Side"),
                                                                 ('right', "Picture on Right Side")],
                            validators=[DataRequired()], default='left')
    title = StringField("Title/Position", validators=[DataRequired()])
    description = TextAreaField("Insert a text here", validators=[DataRequired(), Length(max=365)])
    rank = SelectField("Rank", choices=[], default=0, coerce=int)
    submit = SubmitField('Submit')


class ModifyFeatureForm(FlaskForm):
    """
    The WTForm used to create a new featured story
    """
    left_right = RadioField("Picture on Left or Right", choices=[('left', "Picture on Left Side"),
                                                                 ('right', "Picture on Right Side")],
                            validators=[DataRequired()], default='left')
    title = StringField("Title/Position", validators=[DataRequired()])
    description = TextAreaField("Insert a text here", validators=[DataRequired(), Length(max=365)])
    is_visible = RadioField("Visibility", choices=[('True', "Visible"), ('False', "Not Visible")],
                            validators=[DataRequired()], default='True')
    rank = SelectField("Rank", choices=[], default=0, coerce=int)
    submit = SubmitField('Submit')


class EditTagForm(FlaskForm):
    """
        The WTForm used to edit a tag
    """
    name = StringField(validators=[DataRequired()])
    submit = SubmitField('Submit')
