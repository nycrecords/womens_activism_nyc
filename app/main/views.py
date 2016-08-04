from flask import render_template, redirect, url_for, flash, request
from .. import db
from ..models import *
from . import main
from .. import recaptcha


@main.route('/', methods=['GET', 'POST'])
def index(data=None):

    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.creation_time.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=True)

    posts = pagination.items

    if data or request.method == 'POST':
        if request.form['input_title'] == '':
            if request.form['editor1'] == '':
                return render_template('index.html', posts=posts, pagination=pagination, recaptcha=recaptcha)
            else:
                flash('Please enter a title.')
                return render_template('index.html', posts=posts, pagination=pagination, recaptcha=recaptcha)
        elif request.form['editor1'] == '':
            flash('Please enter content.')
            return render_template('index.html', posts=posts, pagination=pagination, recaptcha=recaptcha)
        elif recaptcha.verify() == False:
            flash("Please complete reCAPTCHA")
            return render_template('index.html', posts=posts, post_title=request.form['input_title'],
                                   post_content=request.form['editor1'], pagination=pagination)
        else:
            title = request.form['input_title']
            content = request.form['editor1']
            post = Post(title=title, content=content, is_edited=False, is_visible=True)
            db.session.add(post)
            db.session.commit()
            flash('Post submitted!')
            return redirect(url_for('.index'))
    return render_template('index.html', posts=posts, pagination=pagination, recaptcha=recaptcha)