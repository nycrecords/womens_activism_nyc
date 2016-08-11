from flask import render_template, redirect, url_for, flash, request
from .. import db
from ..models import *
from . import main
from .. import recaptcha
# from .forms import TagForm


@main.route('/', methods=['GET', 'POST'])
def index(data=None):

    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.creation_time.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=True)

    posts = pagination.items
    tags = Tag.query.all()

    if data or request.method == 'POST':
        print (request.form.getlist('input_tags'))
        if request.form['input_title'] == '':
            if request.form['editor1'] == '':
                return render_template('index.html', posts=posts, pagination=pagination, tags=tags)
            else:
                flash('Please enter a title.')
                return render_template('index.html', posts=posts, pagination=pagination, tags=tags)
        elif request.form['editor1'] == '':
            flash('Please enter content.')
            return render_template('index.html', posts=posts, pagination=pagination, tags=tags)
        elif len(request.form.getlist('input_tags')) == 0:
            flash('Please choose at least one tag.')
            return render_template('index.html', posts=posts, pagination=pagination, tags=tags)
        elif recaptcha.verify() == False:
            flash("Please complete reCAPTCHA")
            return render_template('index.html', posts=posts, post_title=request.form['input_title'],
                                   post_content=request.form['editor1'], pagination=pagination, tags=tags)
        else:
            title = request.form['input_title']
            content = request.form['editor1']
            post = Post(title=title, content=content, is_edited=False, is_visible=True)
            db.session.add(post)
            db.session.commit()

            tag_list = request.form.getlist('input_tags')
            for tag in tag_list:
                post_tag = PostTag(post_id=post.id, tag_id=Tag.query.filter_by(name=tag).id)
                db.session.add(post_tag)
                db.session.commit()
            flash('Post submitted!')
            return redirect(url_for('.index'))
    return render_template('index.html', posts=posts, pagination=pagination, tags=tags)
