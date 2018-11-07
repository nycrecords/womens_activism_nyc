from app.edit import edit
from flask import render_template, redirect, url_for, flash, request, Markup, abort
from app.models import Tags, Stories, Users
from app.edit.forms import StoryForm
from app.edit.utils import update_story, update_user
from app.lib.utils import create_user
from sqlalchemy.orm.exc import NoResultFound
from flask_login import login_required


@edit.route('/<story_id>', methods=['GET', 'POST'])
@login_required
def edit(story_id):
    """
    view function for editing a story
    :param story_id - a story id that has been selected
    """
    story = Stories.query.filter_by(id=story_id).one()
    user = Users.query.filter_by(guid=story.user_guid).one_or_none()
    form = StoryForm(request.form, content=story.content)

    if request.method == 'POST':
        if form.validate_on_submit():
            if user is not None:
                user_guid = update_user(user,
                                        form.user_first.data,
                                        form.user_last.data)

            else:
                user_guid = None
                if form.user_first.data or form.user_last.data:
                    user_guid = create_user(user_first=form.user_first.data,
                                            user_last=form.user_last.data,
                                            user_email=None,
                                            user_phone=None)

            tag_string = form.tags.data
            tags = []
            for t in tag_string.split(','):
                tags.append(Tags.query.filter_by(id=t).one().name)

            story_id = update_story(story_id=story_id,
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
            return render_template('edit/edit.html', story=story, user=user, form=form,
                                   tags=Tags.query.order_by(Tags.name).all())

    else:
        try:
            assert story.is_visible
        except NoResultFound:
            print("Story does not exist")
            return abort(404)
        except AssertionError:
            print("Story is not visible")
            return abort(404)

        return render_template('edit/edit.html', story=story, user=user, form=form, tags=Tags.query.all())
