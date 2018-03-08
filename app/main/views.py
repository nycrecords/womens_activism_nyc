from flask import render_template
from app.main import main
from app.models import Stories, FeaturedStories
from app.constants import module, STORY_GOAL_NUMBER
from sqlalchemy.orm.exc import NoResultFound


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

    try:
        story_list = []
        featured_story = FeaturedStories.query.filter_by(is_visible=True).order_by(FeaturedStories.rank.asc()).all()
        # for each featured story in all featured stories
        for each in featured_story:
            story = Stories.query.filter_by(id=each.story_id).one()
            story_list.append((story, each))

    except NoResultFound:
        featured_story = None
        print("No featured module set")

    return render_template('main/home.html',
                           visible_stories=visible_stories,
                           remaining_stories=remaining_stories,
                           stories=stories,
                           featured_story=story_list)


@main.route('/about', methods=['GET'])
def about():
    return render_template('main/about.html')


@main.route('/contact', methods=['GET'])
def contact():
    return render_template('main/contact.html')