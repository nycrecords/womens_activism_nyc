from flask import render_template, redirect, url_for, flash, request
from ..models import *
from app.main import main
from app.db_helpers import put_obj


@main.route('/', methods=['GET', 'POST'])
def index(data=None):

    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.creation_time.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=True)
    postedit = PostEdit.query.all()

    # need to change this config parameter if I want to change the default 20 posts per page

    posts = pagination.items
    tags = Tag.query.all()
    return render_template('index.html', postedit=postedit, posts=posts, pagination=pagination)


@main.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


@main.route('/archive', methods=['GET', 'POST'])
def archive():
    return render_template('archive.html')


@main.route('/share', methods=['GET', 'POST'])
def share(data=None):
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.creation_time.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=True)
    postedit = PostEdit.query.all()
    posts = pagination.items

    if data or request.method == 'POST':
        if request.form['input_title'] == '':
            if request.form['editor1'] == '':
                flash('Please enter a title.')
                flash('Please enter content.')
                return render_template('index.html', postedit=postedit, posts=posts, pagination=pagination)
            else:
                flash('Please enter a title.')
                return render_template('index.html', postedit=postedit, posts=posts, pagination=pagination)
        elif request.form['editor1'] == '':
            flash('Please enter content.')
            return render_template('index.html', postedit=postedit, posts=posts, pagination=pagination)

        else:
            title = request.form['input_title']
            content = request.form['editor1']
            post = Post(title=title, content=content, is_edited=False, is_visible=True)
            put_obj(post)
            flash('Post submitted!')
            return redirect(url_for('.index'))

    return render_template('share.html')

