"""
WTForms used for Stories
"""
from flask_wtf import Form
from wtforms import TextAreaField, StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Optional, Length, Email

from app.share.validators import (validate_end_year,
                                  validate_image,
                                  validate_start_year,
                                  validate_url,
                                  validate_video)


class StoryForm(Form):
    """
    The WTForm used to create a new Story
    """
    activist_first = StringField("Activist first name", validators=[DataRequired(), Length(1, 30)],
                                 id="first-name-field")
    activist_last = StringField("Activist last name", validators=[DataRequired(), Length(1, 30)], id="last-name-field")
    activist_start = StringField("Activist birth year", validators=[DataRequired(), Length(1, 4), validate_start_year],
                                 id="year-born-input")
    activist_start_BC = BooleanField("Check if activist was born during BC", validators=[Optional()])
    activist_end = StringField("Activist death year", validators=[DataRequired(), Length(1, 5), validate_end_year],
                               id="year-death-input")
    activist_end_BC = BooleanField("Check if activist died during BC", validators=[Optional()])
    tags = StringField(validators=[DataRequired()])
    content = TextAreaField("Share a few words about how your woman activist has inspired you and others",
                            validators=[DataRequired(), Length(1, 5000)], id="her-story-text")
    activist_url = StringField("Enter a URL to allow others to learn more about your woman activist online",
                               validators=[Optional(), Length(1, 254), validate_url], id="activist-url")
    image_url = StringField("Enter an image URL below", validators=[Optional(), Length(1, 254)
                            , validate_image], id="image-url")
    video_url = StringField("Enter a YouTube or Vimeo URL below", validators=[Optional(), validate_video],
                            id="video-url")
    poster_first = StringField("Poster first name", validators=[Optional(), Length(1, 30)], id="user-first-name-field")
    poster_last = StringField("Poster last name", validators=[Optional(), Length(1, 30)], id="user-last-name-field")
    poster_email = StringField("Poster email", validators=[Optional(), Email(), Length(1, 254)], id="user-email-field")
    submit = SubmitField('Submit', id="share-story-btn")
