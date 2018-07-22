from flask import render_template
from app.main import main
from app.models import Stories, FeaturedStories
from app.constants import STORY_GOAL_NUMBER


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

    featured_stories = FeaturedStories.query.filter_by(is_visible=True).all()

    visible_featured_stories = []
    for n in range(len(featured_stories)):
        visible_featured_stories += str(n+1)

    return render_template('main/home.html',
                           visible_stories=visible_stories,
                           remaining_stories=remaining_stories,
                           stories=stories,
                           featured_stories=featured_stories,
                           visible_featured_stories=visible_featured_stories)


@main.route('/about', methods=['GET'])
def about():
    return render_template('main/about.html')


@main.route('/contact', methods=['GET'])
def contact():
    return render_template('main/contact.html')