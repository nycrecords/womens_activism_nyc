from app.edit import edit
from flask import render_template, redirect, url_for, flash, request, Markup, abort
from app.constants import RECAPTCHA_STRING
from app.models import Tags, Stories, Users
from app.edit.forms import StoryForm
from app.edit.utils import edit_story, edit_user
from sqlalchemy.orm.exc import NoResultFound

from flask_login import login_required


@edit.route('/edit/<story_id>', methods=['GET', 'POST'])
@login_required
def test(story_id):
    '''
        view function for editing a story
        :return:
            for now, focus on creating a template for the edit (inherit the template from share)
            and prepopulate the existing values
    '''
    story = Stories.query.filter_by(id=story_id).one()
    user = Users.query.filter_by(guid=story.user_guid).one() if story.user_guid else None
    form = StoryForm(request.form, content=story.content)

    if request.method == 'POST':
        if form.validate_on_submit():
            if form.user_first.data != user.first_name or form.user_last.data != user.last_name or \
                    form.user_email.data != user.email:

                user_guid = edit_user(story_id=story_id,
                                        user_first=form.user_first.data,
                                        user_last=form.user_last.data,
                                        user_email=form.user_email.data)

            else:
                user_guid = story.user_guid

            tag_string = form.tags.data
            tags = []
            for t in tag_string.split(','):
                tags.append(Tags.query.filter_by(id=t).one().name)

            story_id = edit_story(story_id=story_id,
                                  activist_first=form.activist_first.data,
                                  activist_last=form.activist_last.data,
                                  activist_start=form.activist_start.data,
                                  activist_end=form.activist_end.data,
                                  tags=tags,
                                  content=form.content.data,
                                  activist_url=form.activist_url.data,
                                  image_url=form.image_url.data,
                                  video_url=form.video_url.data,
                                  user_guid=user_guid,
                                  reason=form.reason.data)

            flash(Markup('Story Edited!'), category='success')
            return redirect(url_for('stories.view', story_id=story_id))
        else:
            for field, error in form.errors.items():
                flash(form.errors[field][0], category="danger")
            return render_template('edit/edit.html', story=story, user=user, form=form, tags=Tags.query.all())

    try:
        assert story.is_visible
    except NoResultFound:
        print("Story does not exist")
        return abort(404)
    except AssertionError:
        print("Story is not visible")
        return abort(404)

    if story.is_visible:
        return render_template('edit/edit.html', story=story, user=user, form=form, tags=Tags.query.all())