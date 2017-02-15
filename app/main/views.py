from flask import render_template
from app.main import main
from app.models import Stories


@main.route('/', methods=['GET', 'POST'])
def index():
    """
    View function for the homepage. This function queries the database for the amount of current visible stories
    and the 8 most recent stories.
    :return: renders the 'index.html' template with parameters for the current story count and recent stories
    """
    visible_stories = len(Stories.query.filter_by(is_visible=True).all())
    story_counter = 20000 - visible_stories

    all_stories = Stories.query.filter_by(is_visible=True).order_by(Stories.date_created.desc())
    recent_stories = all_stories[:8]

    return render_template('index.html', story_counter=story_counter, recent_stories=recent_stories)