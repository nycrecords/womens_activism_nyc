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
from app.models import Post, Tag, PostTag, PostEdit
from app.main import main
from app import recaptcha


@main.route('/simon', methods=['GET', 'POST'])
def simonindex(data=None):

    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.creation_time.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=True)
    postedit = PostEdit.query.all()

    # need to change this config parameter if I want to change the default 20 posts per page

    posts = pagination.items
    tags = Tag.query.all()
    return render_template('index.html', postedit=postedit, posts=posts, pagination=pagination)


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
    all_tags = Tag.query.all()

    page_posts = []
    """
    page_posts is a list of dictionary containing attributes of posts
    page_posts is used because tags cannot be accessed through posts
    """
    for post in posts:
        post_tags = PostTag.query.filter_by(post_id=post.id).all()
        tags = []
        for post_tag in post_tags:
            name = Tag.query.filter_by(id=post_tag.tag_id).first().name
            tags.append(name)
        story = {
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'time': post.creation_time,
            'comment_count': post.comments.count(),
            'edit_time': post.edit_time,
            'is_visible': post.is_visible,
            'is_edited': post.is_edited,
            'tags': tags
        }
        page_posts.append(story)

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


@main.route('/simonabout', methods=['GET', 'POST'])
def simonabout():
    return render_template('about.html')


@main.route('/simonarchive', methods=['GET', 'POST'])
def simonarchive():
    tags = Tag.query.all()
    return render_template('archive.html', tags=tags)


@main.route('/simonshare', methods=['GET', 'POST'])
def simonshare():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.creation_time.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=True)
    postedit = PostEdit.query.all()
    posts = pagination.items

    data = request.form.copy()
    if data or request.method == 'POST':
        errors = False
        # if data['inspire_name'] == '':
        #     flash('Please enter a name.')
        #     errors = True
        if data['activist_first_name'] == '':
            flash('Please enter their first name.')
            errors = True
        if data['activist_last_name'] == '':
            flash('Please enter their last name.')
            errors = True
        if data['activist_start_date'] == '':
            flash('Please enter a day of birth.')
            errors = True
        if data['activist_end_date'] == '':
            flash('Please enter a death.')
            errors = True
        if data['content'] == '':
            flash('Please share a story.')
            errors = True
        if data['author_first_name'] == '':
            flash('Please enter your first name.')
            errors = True
        if data['author_last_name'] == '':
            flash('Please enter your last name.')
            errors = True
        if data['author_website'] == '':
            flash('Please enter your website.')
            errors = True
        if data['author_email'] == '':
            flash('Please enter your email.')
            errors = True
        # if data['input_email'] == '':
        #     flash('Please enter your email.')
        #     errors = True
        # if data['input_website'] == '':
        #     flash('Please enter your website.')
        #     errors = True
        if errors:
            return render_template('share.html')
# do add media button, images, video and youtube
# feature/wom-20
        activist_first_name = data['activist_first_name'].strip()
        activist_last_name = data['activist_last_name'].strip()
        activist_start_date = data['activist_start_date'].strip()
        activist_end_date = data['activist_end_date'].strip()
        content = data['content'].strip()
        author_first_name = data['author_first_name'].strip()
        author_last_name = data['author_last_name'].strip()
        author_email = data['author_email'].strip()
        author_website = data['author_website'].strip()
        # author_name = data['input_fullname']
        # author_email = data['input_email']
        # author_website = data['input_website']
        # author_name=author_name, author_email=author_email, author_website=author_website,
        post = Post(activist_first_name=activist_first_name, activist_last_name=activist_last_name,
                    activist_start_date=activist_start_date, activist_end_date=activist_end_date, content=content,
                    author_first_name=author_first_name, author_last_name=author_last_name,
                    author_email=author_email, author_website=author_website, is_edited=False, is_visible=True)
        put_obj(post)
        flash('Post submitted!')
        return redirect(url_for('.index'))
    else:
        return render_template('share.html')



