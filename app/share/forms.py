"""
WTForms used for Stories
"""
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    FileField,
    TextAreaField,
    StringField,
    SubmitField,
)

from wtforms.validators import (
    DataRequired,
    Optional,
    Length,
    Email,
)

from app.share.validators import (validate_end_year,
                                  validate_image,
                                  validate_start_year,
                                  validate_url,
                                  validate_video)


class StoryForm(FlaskForm):
    """
    The WTForm used to create a new Story
    """
    activist_first = StringField("Activist first name", validators=[DataRequired(), Length(1, 64)])
    activist_last = StringField("Activist last name", validators=[DataRequired(), Length(1, 64)])
    activist_start = StringField("Activist birth year", validators=[Optional(), Length(1, 4), validate_start_year])
    activist_end = StringField("Activist death year", validators=[Optional(), Length(1, 5), validate_end_year])
    tags = StringField(validators=[DataRequired(), Length(1, 500)])
    content = TextAreaField("Share a few words about how your woman activist has inspired you and others",
                            validators=[DataRequired()])
    image_url = StringField("Enter an image URL below", validators=[Optional(), validate_image])
    image_pc = FileField()
    activist_url = StringField("Enter a URL to allow others to learn more about your woman activist online",
                               validators=[Optional(), validate_url])
    video_url = StringField("Enter a YouTube or Vimeo URL below", validators=[Optional(), validate_video])
    user_first = StringField("User first name", validators=[Optional(), Length(1, 128)])
    user_last = StringField("User last name", validators=[Optional(), Length(1, 128)])
    user_email = StringField("User email", validators=[Optional(), Email(), Length(1, 254)])
    user_phone = StringField("User phone number", validators=[Optional(), Length(1, 25)])
    subscription = BooleanField("Subscription")
    submit = SubmitField('Submit')
