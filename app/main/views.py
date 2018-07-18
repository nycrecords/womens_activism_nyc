from flask import render_template, redirect, url_for, flash, request, Markup
from app.main import main
from app.models import Stories, FeaturedStories
from app.constants import STORY_GOAL_NUMBER
from app.share.forms import StoryForm
from app.share.utils import create_user
from app.constants import RECAPTCHA_STRING


@main.route('/', methods=['GET'])
def index():
    """
    View function for the homepage. This function queries the database for the amount of current visible stories
    and the 8 most recent stories.
    :return: renders the 'index.html' template with parameters for the current story count and recent stories
    """
    visible_stories = len(Stories.query.filter_by(is_visible=True).all())
    remaining_stories = STORY_GOAL_NUMBER - visible_stories

    stories = Stories.query.filter_by(is_visible=True).order_by(Stories.date_created.desc()).limit(8)

    featured_story = FeaturedStories.query.filter_by(is_visible=True).one_or_none()

    return render_template('main/home.html',
                           visible_stories=visible_stories,
                           remaining_stories=remaining_stories,
                           stories=stories,
                           featured_story=featured_story)


@main.route('/about', methods=['GET'])
def about():
    return render_template('main/about.html')


@main.route('/contact', methods=['GET'])
def contact():
    return render_template('main/contact.html')

@main.route('/subscribe', methods=['GET','POST'])
def subscribe():
        #return render_template('main/subscribe.html')
    form = StoryForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            if form.user_first.data or form.user_last.data or form.user_email.data:
                user_guid = create_user(user_first=form.user_first.data,
                                        user_last=form.user_last.data,
                                        user_email=form.user_email.data,
                                        user_phone= form.user_phone.data,
                                        subscription=form.subscription.data)
            else:
                user_guid = None
        
            return render_template('main/subscribe.html', form=form)
    return render_template('main/subscribe.html', form=form)