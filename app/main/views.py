from flask import render_template, redirect, url_for, flash, request
from ..models import *
from app.main import main
from app.db_helpers import put_obj


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


@main.route('/simonabout', methods=['GET', 'POST'])
def simonabout():
    return render_template('about.html')


@main.route('/simonarchive', methods=['GET', 'POST'])
def simonarchive():
    return render_template('archive.html')


@main.route('/simonshare', methods=['GET', 'POST'])
def simonshare():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.creation_time.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=True)
    postedit = PostEdit.query.all()
    posts = pagination.items
# fix changes here
    # do changes here
    # for post in posts:
    #     id = post.id
    #     activist_name = post.inspire_name
    #     activist_start_date = post.input_birth
    #     activist_end_date = post.input_death
    #     content = post.editor1
    #     author_name = post.input_fullname
    #     author_email = post.input_email
    #     author_website = post.website
    #     author_name = post.input_fullname
    #     just_now = post.just_now()
    #     time = post.creation_time
    #     comment_count = post.comments.count()
    #     edit_time = post.edit_time
    #     is_visible = post.is_visible
    #     is_edited = post.is_edited

    data = request.form.copy()
    if data or request.method == 'POST':
        errors = False
        if data['inspire_name'] == '':
            flash('Please enter a name.')
            errors = True
        if data['input_birth'] == '':
            flash('Please enter a day of birth.')
            errors = True
        if data['input_death'] == '':
            flash('Please enter a death.')
            errors = True
        if data['editor1'] == '':
            flash('Please share a story.')
            errors = True
        if data['input_fullname'] == '':
            flash('Please enter your full name.')
            errors = True
        if data['input_email'] == '':
            flash('Please enter your email.')
            errors = True
        if data['input_website'] == '':
            flash('Please enter your website.')
            errors = True

        if errors:
            return render_template('share.html')

        activist_name = data['inspire_name']
        activist_start_date = data['input_birth']
        activist_end_date = data['input_death']
        content = data['editor1']
        author_name = data['input_fullname']
        author_email = data['input_email']
        author_website = data['input_website']
        post = Post(activist_name=activist_name, activist_start_date=activist_start_date,
                    activist_end_date=activist_end_date, author_name=author_name, author_email=author_email,
                    author_website=author_website, content=content, is_edited=False, is_visible=True)
        put_obj(post)
        flash('Post submitted!')
        return redirect(url_for('.index'))
    else:
        return render_template('share.html')

