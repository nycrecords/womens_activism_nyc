"""
Modules needed for main/views.py
flask:
    used render_template to load templates
    used redirect to redirect to specific url
    used url_for to designate the specific url
    used current_app for config data variables
    used flash to send messages to the user
    used request to get information from the ckeditor html form in index.html
app.db_helpers:
    used to add and commit sessions for Post with the put_obj() function
app.models:
    used Post table to add of data every time user successfully submitted a post
    used Tag table to provide a list of tags to decide from when creating a post
app.main:
    used to import the main blueprint where routes are identified from
app:
    used recaptcha for verification purposes - prevent bot spam
"""
from flask import render_template, redirect, url_for, flash, request, current_app
from app.db_helpers import put_obj
from app.models import Post, Tag
from app.main import main
from app import recaptcha


@main.route('/', methods=['GET', 'POST'])
def index(data=None):
    """
    query the database for a feed of most recent posts
    query the database for the list of possible tags - passed into drop down selectfield in html
    :param data: initialized as none because we want a blank form to appear when user first loads page
    :return: renders template that displays a ckeditor where user can start writing their post.
        Second half of the page is a feed of most recent posts
    """

    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.creation_time.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=True)

    posts = pagination.items
    tags = Tag.query.all()

    if data or request.method == 'POST':  # user presses the submit button
        if request.form['input_title'] == '':  # user has not entered a title
            if request.form['editor1'] == '':  # user has not entered any information into both fields
                return render_template('index.html', posts=posts, pagination=pagination, tags=tags)
            else:
                flash('Please enter a title.')
                return render_template('index.html', posts=posts, pagination=pagination, tags=tags)
        elif request.form['editor1'] == '':  # user has not entered a description/content
            flash('Please enter content.')
            return render_template('index.html', posts=posts, pagination=pagination, tags=tags)
        elif recaptcha.verify() == False:  # user has not passed the recaptcha verification
            flash("Please complete reCAPTCHA")
            return render_template('index.html', posts=posts, post_title=request.form['input_title'],
                                   post_content=request.form['editor1'], pagination=pagination, tags=tags)
        else:  # successful submission of the post
            title = request.form['input_title']
            content = request.form['editor1']
            tags = request.form['tags']
            ### Todo: get tags associated with posts

            post = Post(title=title, content=content, is_edited=False, is_visible=True)
            put_obj(post)
            flash('Post submitted!')
            return redirect(url_for('.index'))
    return render_template('index.html', posts=posts, pagination=pagination, tags=tags)
