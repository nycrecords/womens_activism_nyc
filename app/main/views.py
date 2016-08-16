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
from app.models import User, Story, Tag, StoryTag
from app.main import main
from app import recaptcha


# @main.route('/simon', methods=['GET', 'POST'])
# # TODO: Delete this route, we don't need it anymore - any changes made by simon needs to be implemented into index.html
# def simonindex(data=None):
#     page = request.args.get('page', 1, type=int)
#     pagination = Story.query.order_by(Story.creation_time.desc()).paginate(
#         page, per_page=current_app.config['POSTS_PER_PAGE'],
#         error_out=True)
#     posts = pagination.items
#
#     page_posts = []
#
#     for post in posts:
#         post_tags = PostTag.query.filter_by(post_id=post.id).all()
#         tags = []
#         for post_tag in post_tags:
#             name = Tag.query.filter_by(id=post_tag.tag_id).first().name
#             tags.append(name)
#         story = {
#             'id': post.id,
#             'activist_first': post.activist_first,
#             'activist_last': post.activist_last,
#             'activist_start': post.activist_start,
#             'activist_end': post.activist_end,
#             'creation_time': post.creation_time,
#             'edit_time': post.edit_time,
#             'content': post.content,
#             'is_visible': post.is_visible,
#             'is_edited': post.is_edited,
#             'tags': tags
#         }
#         page_posts.append(story)
#
#     return render_template('new_index.html', posts=page_posts, pagination=pagination)


@main.route('/', methods=['GET', 'POST'])
def index(data=None):
    """
    query the database for a feed of most recent posts
    query the database for the list of possible tags - passed into drop down selectfield in html
    :param data: initialized as none because we want a blank form to appear when user first loads page
    :return: renders template that displays a ckeditor where user can start writing their post.
        Second half of the page is a feed of most recent posts
    """
    # TODO: Update docstring, should not be able to post on index html - instead this should be a new html file in templates/posts/new_story
    page = request.args.get('page', 1, type=int)
    pagination = Story.query.order_by(Story.creation_time.desc()).paginate(
        page, per_page=current_app.config['STORIES_PER_PAGE'],
        error_out=True)

    stories = pagination.items
    all_tags = Tag.query.all()

    page_stories = []
    """
    page_posts is a list of dictionary containing attributes of posts
    page_posts is used because tags cannot be accessed through posts
    """
    for story in stories:
        story_tags = StoryTag.query.filter_by(story_id=story.id).all()
        tags = []
        for story_tag in story_tags:
            name = Tag.query.filter_by(id=story_tag.tag_id).first().name
            tags.append(name)
        story = {
            'id': story.id,
            'title': story.title,
            'content': story.content,
            'time': story.creation_time,
            'edit_time': story.edit_time,
            'is_visible': story.is_visible,
            'is_edited': story.is_edited,
            'tags': tags
        }
        page_stories.append(story)

    if data or request.method == 'POST':  # user presses the submit button
        data = request.form.copy()
        if data['input_title'] == '':  # user has not entered a title
            if data['editor1'] == '':  # user has not entered any information into both fields
                return render_template('index.html', posts=page_posts, post_title=data['input_title'],
                                       post_content=data['editor1'], pagination=pagination, tags=all_tags)
            else:
                flash('Please enter a title.')
                return render_template('index.html', posts=page_posts, post_title=data['input_title'],
                                       post_content=data['editor1'], pagination=pagination, tags=all_tags)
        elif data['editor1'] == '':  # user has not entered a description/content
            flash('Please enter content.')
            return render_template('index.html', posts=page_posts, post_title=data['input_title'],
                                   post_content=data['editor1'], pagination=pagination, tags=all_tags)
        elif len(request.form.getlist('input_tags')) == 0:
            flash('Please choose at least one tag.')
            return render_template('index.html', posts=page_posts, pagination=pagination, tags=all_tags)
        elif recaptcha.verify() == False:  # user has not passed the recaptcha verification
            flash("Please complete reCAPTCHA")
            return render_template('index.html', posts=page_posts, post_title=data['input_title'],
                                   post_content=data['editor1'], pagination=pagination, tags=all_tags)
        else:  # successful submission of the post
            title = data['input_title']
            content = data['editor1']

            post = Post(title=title, content=content, is_edited=False, is_visible=True)
            put_obj(post)

            tag_list = request.form.getlist('input_tags')
            for tag in tag_list:
                post_tag = PostTag(post_id=post.id, tag_id=Tag.query.filter_by(name=tag).first().id)
                put_obj(post_tag)
            flash('Post submitted!')
            print(page_posts)
            return redirect(url_for('.index'))
    return render_template('index.html', posts=page_posts, pagination=pagination, tags=all_tags)

# @main.route('/simonabout', methods=['GET', 'POST'])
# def simonabout():
#     # TODO: rename this route
#     return render_template('about.html')
#
#
# @main.route('/simonarchive', methods=['GET', 'POST'])
# def simonarchive():
#     # TODO: rename this route and put it into posts/views.py
#     # TODO: edit archive.html to have the contents of postTab.html and then delete postTab.html
#     tags = Tag.query.all()
#     return render_template('archive.html', tags=tags)
#
#
# @main.route('/simonshare', methods=['GET', 'POST'])
# def simonshare():
#     # TODO: rename this route and put it into posts/views.py
#     tags = Tag.query.all()
#     data = request.form.copy()
#
#     if data or request.method == 'POST':
#
#         activist_first_name = data['activist_first_name'].strip()
#         activist_last_name = data['activist_last_name'].strip()
#         activist_start_date = data['input_birth'].strip()
#         activist_end_date = data['input_death'].strip()
#         content = data['editor1'].strip()
#         author_first_name = data['author_first_name'].strip()
#         author_last_name = data['author_last_name'].strip()
#         author_email = data['input_email'].strip()
#         errors = False
#
#         if activist_first_name == '':
#             flash("Please enter a first name for women's activist.")
#             errors = True
#         if activist_last_name == '':
#             flash("Please enter a last name for women's activist.")
#             errors = True
#         if activist_start_date == '':
#             flash("Please enter a year of birth for women's activist.")
#             errors = True
#         if activist_end_date == '':
#             flash("Please enter a year of death for women's activist.")
#             errors = True
#         if content == '':
#             flash('Please enter a story.')
#             errors = True
#         if author_first_name == '':
#             flash('Please enter your first name.')
#             errors = True
#         if author_last_name == '':
#             flash('Please enter your last name.')
#             errors = True
#         if author_email == '':
#             flash('Please enter your email.')
#             errors = True
#         if errors:
#             return render_template('share.html')
#
#         post = Post(activist_start=activist_start_date, activist_end=activist_end_date,
#                     activist_first=author_first_name, activist_last=author_last_name, content=content,
#                     author_first=author_first_name, author_last=author_last_name, is_edited=False, is_visible=True)
#         put_obj(post)
#
#         if len(author_first_name.strip()) > 0 or len(author_last_name.strip()) > 0 or (author_email.strip()) > 0:
#             user = User(first_name=author_first_name, last_name=author_last_name, email=author_email)
#             put_obj(user)
#
#         flash('Post submitted!')
#         return redirect(url_for('.index'))
#     else:
#         return render_template('share.html', tags=tags)
