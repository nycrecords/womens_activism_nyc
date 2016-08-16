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
from app.models import User, Post, Tag, PostTag
from app.main import main
from app import recaptcha


@main.route('/', methods=['GET', 'POST'])
# TODO: Delete this route, we don't need it anymore - any changes made by simon needs to be implemented into index.html
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.creation_time.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=True)
    posts = pagination.items

    page_posts = []

    for post in posts:
        post_tags = PostTag.query.filter_by(post_id=post.id).all()
        tags = []
        for post_tag in post_tags:
            name = Tag.query.filter_by(id=post_tag.tag_id).first().name
            tags.append(name)
        story = {
            'id': post.id,
            'activist_first': post.activist_first,
            'activist_last': post.activist_last,
            'activist_start': post.activist_start,
            'activist_end': post.activist_end,
            'creation_time': post.creation_time,
            'edit_time': post.edit_time,
            'content': post.content,
            'is_visible': post.is_visible,
            'is_edited': post.is_edited,
            'tags': tags
        }
        page_posts.append(story)

    return render_template('new_index.html', posts=page_posts, pagination=pagination)


@main.route('/about', methods=['GET', 'POST'])
def about():
    # TODO: rename this route
    return render_template('about.html')


@main.route('/catalog', methods=['GET', 'POST'])
def catalog():
    # TODO: rename this route and put it into posts/views.py
    # TODO: edit catalog.html to have the contents of postTab.html and then delete postTab.html
    tags = Tag.query.all()
    return render_template('catalog.html', tags=tags)


@main.route('/shareastory', methods=['GET', 'POST'])
def shareastory(data=None):
    # TODO: rename this route and put it into posts/views.py
    tags = Tag.query.all()

    if data or request.method == 'POST':
        data = request.form.copy()

        activist_first_name = data['activist_first_name']
        activist_last_name = data['activist_last_name']
        activist_start_date = data['input_birth']
        activist_end_date = data['input_death']
        content = data['editor1']
        activist_link = data['input_url_link']
        author_first_name = data['author_first_name']
        author_last_name = data['author_last_name']
        author_email = data['author_email']

        if activist_first_name == '':
            flash("Please enter a first name for women's activist.")
            return render_template('share.html', tags=tags, activist_first_name=activist_first_name,
                                   activist_last_name=activist_last_name, activist_start_date=activist_start_date,
                                   activist_end_date=activist_end_date, content=content, activist_link=activist_link,
                                   author_first_name=author_first_name, author_last_name=author_last_name,
                                   author_email=author_email)
        elif activist_last_name == '':
            flash("Please enter a last name for women's activist.")
            return render_template('share.html', tags=tags, activist_first_name=activist_first_name,
                                   activist_last_name=activist_last_name, activist_start_date=activist_start_date,
                                   activist_end_date=activist_end_date, content=content, activist_link=activist_link,
                                   author_first_name=author_first_name, author_last_name=author_last_name,
                                   author_email=author_email)
        elif activist_start_date == '':
            flash("Please enter a year of birth for women's activist.")
            return render_template('share.html', tags=tags, activist_first_name=activist_first_name,
                                   activist_last_name=activist_last_name, activist_start_date=activist_start_date,
                                   activist_end_date=activist_end_date, content=content, activist_link=activist_link,
                                   author_first_name=author_first_name, author_last_name=author_last_name,
                                   author_email=author_email)
        elif activist_end_date == '':
            flash("Please enter a year of death for women's activist.")
            return render_template('share.html', tags=tags, activist_first_name=activist_first_name,
                                   activist_last_name=activist_last_name, activist_start_date=activist_start_date,
                                   activist_end_date=activist_end_date, content=content, activist_link=activist_link,
                                   author_first_name=author_first_name, author_last_name=author_last_name,
                                   author_email=author_email)
        elif len(activist_end_date) == 5 and activist_end_date != 'Today':
            flash("Please enter a valid year of death for women's activist.")
            return render_template('share.html', tags=tags, activist_first_name=activist_first_name,
                                   activist_last_name=activist_last_name, activist_start_date=activist_start_date,
                                   activist_end_date=activist_end_date, content=content, activist_link=activist_link,
                                   author_first_name=author_first_name, author_last_name=author_last_name,
                                   author_email=author_email)
        elif content == '':
            flash('Please enter a story.')
            return render_template('share.html', tags=tags, activist_first_name=activist_first_name,
                                   activist_last_name=activist_last_name, activist_start_date=activist_start_date,
                                   activist_end_date=activist_end_date, content=content, activist_link=activist_link,
                                   author_first_name=author_first_name, author_last_name=author_last_name,
                                   author_email=author_email)
        elif recaptcha.verify() == False:  # user has not passed the recaptcha verification
            flash("Please complete reCAPTCHA.")
            return render_template('share.html', tags=tags)

        else:
            post = Post(activist_start=activist_start_date, activist_end=activist_end_date,
                        activist_first=activist_first_name, activist_last=activist_last_name, content=content,
                        activist_link=activist_link, author_first=author_first_name, author_last=author_last_name,
                        is_edited=False, is_visible=True)
            put_obj(post)

            if len(author_first_name) > 0 or len(author_last_name) > 0 or len(author_email) > 0:
                user = User(first_name=author_first_name, last_name=author_last_name, email=author_email)
                put_obj(user)

            flash('Post submitted!')
            return redirect(url_for('.index'))
    return render_template('share.html', tags=tags)
