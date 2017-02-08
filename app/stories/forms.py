"""
WTForms used for Stories
"""

from flask_wtf import Form
from wtforms import TextAreaField, StringField, SubmitField, SelectMultipleField, BooleanField
from wtforms.validators import DataRequired, Optional, Length, Email
from app.constants import tag
from app.stories.validators import (validate_name,
                                    validate_white_space,
                                    validate_end_year,
                                    validate_image,
                                    validate_start_year,
                                    validate_url,
                                    validate_video)


class StoryForm(Form):
    """

    """
    activist_first = StringField("Activist first name", validators=[DataRequired(), Length(1, 30),
                                                                    validate_name, validate_white_space],
                                 render_kw={"placeholder": "Mary"})
    activist_last = StringField("Activist last name", validators=[DataRequired(), Length(1, 30),
                                                                  validate_name, validate_white_space],
                                render_kw={"placeholder": "Smith"})
    activist_start = StringField("Activist birth year", validators=[DataRequired(), Length(1, 4),
                                                                    validate_start_year, validate_white_space],
                                render_kw={"placeholder": "1960"})
    activist_start_BC = BooleanField("Check if activist was born during BC", validators=[Optional()])
    activist_end = StringField("Activist death year", validators=[DataRequired(), Length(1, 5),
                                                                  validate_end_year, validate_white_space],
                               render_kw={"placeholder": "Today"})
    activist_end_BC = BooleanField("Check if activist died during BC", validators=[Optional()])
    tags = SelectMultipleField("What is she known for? Choose one or more categories", choices=tag.tag_choices)
    content = TextAreaField("Share a few words about how your woman activist has inspired you and others",
                            validators=[DataRequired(), Length(1, 5000), validate_white_space],
                            render_kw={"placeholder": "Enter your story here"})
    activist_url = StringField("Enter a URL to allow others to learn more about your woman activist online",
                               validators=[Optional(), Length(1, 254), validate_url]
                               , render_kw={"placeholder": "www.activistwoman.com"})
    image_url = StringField("Enter an image URL below", validators=[Optional(), Length(1, 254)
                            , validate_image])
    video_url = StringField("Enter a YouTube or Vimeo URL below", validators=[Optional(), validate_video])
    poster_first = StringField("Poster first name", validators=[Optional(), Length(1, 30), validate_name],
                               render_kw={"placeholder": "Mary"})
    poster_last = StringField("Poster last name", validators=[Optional(), Length(1, 30), validate_name],
                              render_kw={"placeholder": "Smith"})
    poster_email = StringField("Poster email", validators=[Optional(), Email(), Length(1, 254)],
                               render_kw={"placeholder": "msmith@gmail.com"})
    submit = SubmitField('Submit')


class MyForm(Form):
    content = TextAreaField("Share a few words about how your woman activist has inspired you and others",
                            validators=[DataRequired(), Length(1, 5000), validate_white_space],
                            render_kw={"placeholder": "Enter your story here"})
    submit = SubmitField('Submit')
