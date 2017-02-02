"""
Modules needed for flags/views.py
flask:
    used render_template to load templates
    used redirect to redirect to specific url
    used url_for to designate the specific url
    used current_app for config data variables
    used flash to send messages to the user
app.db_helpers:
    used to add and commit sessions for Flags with the put_obj() function
app.models:
    used Flag table to add a row of data every time user successfully submitted flag
    used Story table to call in the information pertaining to a specific story
app.send_email:
    send_email() function defined in app/send_email.py used to send email to recipient, formats subject title and email content
app.flags:
    used to import the flags blueprint where routes are identified from
app.flags.forms:
    used FlagsForm to define object based upon the class FlagsForms created in flags/forms.py
"""
from flask import render_template, redirect, url_for, current_app, flash
from app.db_helpers import put_obj
from app.models import Flag, Story
from app.send_email import send_email
from app.flags import flags
from app.utils import flag_choices
# from app.flags.forms import FlagsForm


@flags.route('/flag/stories/<int:id>', methods=['GET', 'POST'])
def flag_story(id):
    """
    Function flag_story will allow user to provide a type and reason of why they think a post shouldn't be there
    The view function will then commit the information of the flag to the database
    An email will be sent to the email account of WOMENS_ADMIN detailing the information user provided
    User also cannot submit the form if type for flagging "Other" is selected along with a reason length of less than
        50 characters
    :param id: identifies the story that is currently being flagged
    :return: template that renders a form where user will provide their reasoning and issues with the post
    redirects user back to main page when completed
    """
    story = Story.query.get_or_404(id)
    # form = FlagsForm()
    # if form.validate_on_submit():
    #     if (form.flag_type.data == "Other") and (len(form.flag_reason.data) < 50):
    #         flash('Type "Other" requires a description of 50 or more characters.')
    #         flash('Please resubmit your flag ticket.')
    #         return render_template('flags/flags.html', form=form,
    #                                activist_first=activist_first, activist_last=activist_last)
    #     else:
    #         flash('Thank you for your input, a moderator has been notified.')
    #         flag_story = Flag(story_id=story.id, type=form.flag_type.data, reason=form.flag_reason.data)
    #         put_obj(flag_story)
    #         send_email(to=current_app.config['WOMENS_ADMIN'], subject='Flagged Story', template='mail/email_flags',
    #                    activist_first=activist_first, activist_last=activist_last,
    #                    type=flag_story.type, reason=flag_story.reason, story=story)
    #         return redirect(url_for('main.index'))
    # return render_template('flags/flags.html', flag_types=flag_choices, story=story)
    return render_template('404.html')
