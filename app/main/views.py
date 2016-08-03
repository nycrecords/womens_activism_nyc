from flask import render_template, redirect, url_for, current_app, flash, request
from .. import db
from ..models import *
from . import main


@main.route('/', methods=['GET', 'POST'])
def index(data=None):

    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.creation_time.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=True)
    # need to change this config parameter if I want to change the default 20 posts per page
    posts = pagination.items

    if data or request.method == 'POST':
        if request.form['input_title'] == '':
            if request.form['editor1'] == '':
                flash('Please enter a title.')
                flash('Please enter content.')
                return render_template('index.html', posts=posts, pagination=pagination)
            else:
                flash('Please enter a title.')
                return render_template('index.html', posts=posts, pagination=pagination)
        elif request.form['editor1'] == '':
            flash('Please enter content.')
            return render_template('index.html', posts=posts, pagination=pagination)
        else:
            title = request.form['input_title']
            content = request.form['editor1']
            post = Post(title=title, content=content, is_edited=False, is_visible=True)
            #print(db.func.current_timestamp())
            #print(datetime.utcnow())
            db.session.add(post)
            db.session.commit()
            flash('Post submitted!')
            return redirect(url_for('.index'))
    #posts = Post.query.order_by(Post.creation_time.desc()).all()
    return render_template('index.html', posts=posts, pagination=pagination)

