from app.edit import edit
from flask import render_template, redirect, url_for, flash, request, Markup, abort
from app.constants import RECAPTCHA_STRING
from app.models import Tags, Stories, Users
from app.edit.forms import StoryForm
from app.edit.utils import edit_story, edit_user
from sqlalchemy.orm.exc import NoResultFound
from app.constants.video_url import (
    YOUTUBE_FULL_URL,
    YOUTUBE_FULL_URL_SPLIT,
    YOUTUBE_EMBED_URL,
    YOUTUBE_SHORT_URL,
    VIMEO_STRING,
    VIMEO_URL,
    VIMEO_EMBED_URL
)

@edit.route('/edit/<story_id>', methods=['GET', 'POST'])
def test(story_id):
    '''
        view function for editing a story
        :return:
            for now, focus on creating a template for the edit (inherit the template from share)
            and prepopulate the existing values
        '''

    '''
    The cycle:
        Submission success:
            if validate the form (check if creator inputted firstname, lastname, email address)
              create new user // we will call it edit_user for now
            else 
                user_guid = None

            Add all the tags into an array by first splitting them 

            Create a new story // we will call it edit_story for now

            Flash 'success'

            redirect to the stories view page by passing the story_id

        Submission failed:
            check the recaptcha
            check the unfulfilled ones
    '''
    form = StoryForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            if form.user_first.data or form.user_last.data or form.user_email.data:
                user_guid = edit_user(user_first=form.user_first.data,
                                      user_last=form.user_last.data,
                                      user_email=form.user_email.data)
            else:
                user_guid = None

            tag_string = form.tags.data
            tags = []
            for t in tag_string.split(','):
                tags.append(Tags.query.filter_by(id=t).one().name)

            story_id = edit_story(activist_first=form.activist_first.data,
                                  activist_last=form.activist_last.data,
                                  activist_start=form.activist_start.data,
                                  activist_end=form.activist_end.data,
                                  tags=tags,
                                  content=form.content.data,
                                  activist_url=form.activist_url.data,
                                  image_url=form.image_url.data,
                                  video_url=form.video_url.data,
                                  user_guid=user_guid)
            flash(Markup('Story Edited!'), category='success')
            return redirect(url_for('stories.view', story_id=story_id))
        else:
            for field, error in form.errors.items():
                if field == RECAPTCHA_STRING:
                    flash('Please complete the Recaptcha to edit your story.', category="danger")
                else:
                    flash(form.errors[field][0], category="danger")
            return render_template('edit/edit.html', form=form, tags=Tags.query.all())
    return render_template('edit/edit.html', form=form, tags=Tags.query.all())


    try:
        story = Stories.query.filter_by(id=story_id).one()
        assert story.is_visible
    except NoResultFound:
        print("Story does not exist")
        return abort(404)
    except AssertionError:
        print("Story is not visible")
        return abort(404)

    if story.is_visible:
        user = Users.query.filter_by(guid=story.user_guid).one() if story.user_guid else None

        video_url = None
        if story.video_url:
            video_url = story.video_url
            if YOUTUBE_FULL_URL in video_url:
                split = video_url.split(YOUTUBE_FULL_URL_SPLIT, 1)
                video_url = YOUTUBE_EMBED_URL.format(split[1])
            elif YOUTUBE_SHORT_URL in video_url:
                split = video_url.split(YOUTUBE_SHORT_URL, 1)
                video_url = YOUTUBE_EMBED_URL.format(split[1])
            elif VIMEO_STRING in video_url:
                split = video_url.split(VIMEO_URL, 1)
                video_url = VIMEO_EMBED_URL.format(split[1])
        return render_template('edit/edit.html', form=form, tags=Tags.query.all())


    # return render_template('edit/edit.html', story=story, user=user, video_url=video_url