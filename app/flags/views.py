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
    used Flags table to add a row of data every time user successfully submitted flag
    used Post table to call in the information pertaining to a specific post
    used Comment table to call in the information pertaining to a specific comment
app.send_email:
    send_email() function defined in app/send_email.py used to send email to recipient, formats subject title and email content
app.flags:
    used to import the flags blueprint where routes are identified from
app.flags.forms:
    used FlagsForm to define object based upon the class FlagsForms created in flags/forms.py
"""
from flask import render_template, redirect, url_for, current_app, flash
from app.db_helpers import put_obj
from app.models import Flag, Post, Comment
from app.send_email import send_email
from app.flags import flags
from app.flags.forms import FlagsForm


@flags.route('/flag/posts/<int:id>', methods=['GET', 'POST'])
def flag_post(id):
    """
    Function flag_post will allow user to provide a reason and description of why they think a post shouldn't be there
    The view function will then commit the information of the flag to the database
    An email will be sent to the email account of WOMENS_ADMIN detailing the information user provided
    User also cannot submit the form if reason for flagging "Other" is selected along with a description of less than
        50 characters
    :param id: identifies the post that is currently being flagged
    :return: template that renders a form where user will provide their reasoning and issues with the post
    redirects user back to main page when completed
    """
    # TODO: Change post_title to activist first, last . . . . etc
    post = Post.query.get_or_404(id)
    post_title = post.title
    form = FlagsForm()
    if form.validate_on_submit():
        if (form.flag_reason.data == "Other") and (len(form.flag_description.data) < 50):
            flash('Reason "Other" requires a description of 50 or more characters.')
            flash('Please resubmit your flag ticket.')
            return render_template('flags/flags.html', form=form, post_title=post_title)
        else:
            flash('Thank you for your input, a moderator has been notified.')
            flag_post = Flag(post_id=post.id,
                             type=form.flag_reason.data,
                             reason=form.flag_description.data)
            put_obj(flag_post)
            send_email(to=current_app.config['WOMENS_ADMIN'], subject='Flagged Post', template='mail/email_flags',
                       post_title=post_title, post=post, reason=flag_post.type, description=flag_post.reason)
            return redirect(url_for('main.index'))
    return render_template('flags/flags.html', form=form, post_title=post_title)


# @flags.route('/flag/posts/<int:id>/comments/<int:id2>', methods=['GET', 'POST'])
# def flag_comment(id, id2):
#     """
#         Function flag_comment will allow user to provide a reason and description of why they think a comment on a post shouldn't be there
#         The view function will then commit the information of the flag to the database
#         An email will be sent to the email account of WOMENS_ADMIN detailing the information user provided
#         User also cannot submit the form if reason for flagging "Other" is selected along with a description of less than
#             50 characters
#         :param id: identifies the post that is currently being flagged
#         :return: template that renders a form where user will provide their reasoning and issues with the comment of a post
#         redirects user back to main page when completed
#         """
#     post = Post.query.get_or_404(id)
#     comment = Comment.query.get_or_404(id2)
#     post_title = post.title
#     comment_content = comment.content
#     form = FlagsForm()
#     if form.validate_on_submit():
#         if (form.flag_reason.data == "Other") and (len(form.flag_description.data) < 50):
#             flash('Reason "Other" requires a description of 50 or more characters.')
#             flash('Please resubmit your flag ticket.')
#             return render_template('flags/flags.html',
#                                    form=form, post_title=post_title, comment_content=comment_content)
#         else:
#             flash('Thank you for your input, a moderator has been notified.')
#             flag_comment = Flag(post_id=post.id,
#                                 comment_id=comment.id,
#                                 type=form.flag_reason.data,
#                                 reason=form.flag_description.data)
#             put_obj(flag_comment)
#             send_email(to=current_app.config['WOMENS_ADMIN'], subject='Flagged Comment', template='mail/email_flags',
#                        post_title=post_title, post=post, comment_content=comment.content,
#                        reason=flag_comment.type, description=flag_comment.reason)
#             return redirect(url_for('posts.posts', id=post.id, _external=True))
#     return render_template('flags/flags.html', form=form, post_title=post_title, comment_content=comment_content)
