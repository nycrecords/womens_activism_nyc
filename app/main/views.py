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
    all_tags = Tag.query.all()

    page_posts = []

    for post in posts:
        id = post.id
        title = post.title
        content = post.content
        just_now = post.just_now()
        time = post.creation_time
        comment_count = post.comments.count()

        post_tags = PostTag.query.filter_by(post_id=post.id).all()
        tags = []
        for post_tag in post_tags:
            name = Tag.query.filter_by(id=post_tag.tag_id).first().name
            tags.append([post_tag.tag_id, name])
        page_posts.append([id, title, content, just_now, time, comment_count, tags])
    if data or request.method == 'POST':
        if request.form['input_title'] == '':
            if request.form['editor1'] == '':
                return render_template('index.html', posts=page_posts, pagination=pagination, tags=all_tags)
            else:
                flash('Please enter a title.')
                return render_template('index.html', posts=page_posts, pagination=pagination, tags=all_tags)
        elif request.form['editor1'] == '':
            flash('Please enter content.')
            return render_template('index.html', posts=page_posts, pagination=pagination, tags=all_tags)
        elif len(request.form.getlist('input_tags')) == 0:
            flash('Please choose at least one tag.')
            return render_template('index.html', posts=page_posts, pagination=pagination, tags=all_tags)
        # elif recaptcha.verify() == False:
        #     flash("Please complete reCAPTCHA")
        #     return render_template('index.html', posts=page_posts, post_title=request.form['input_title'],
        #                            post_content=request.form['editor1'], pagination=pagination, tags=all_tags)
        else:
            title = request.form['input_title']
            content = request.form['editor1']
            post = Post(title=title, content=content, is_edited=False, is_visible=True)
            db.session.add(post)
            db.session.commit()

            tag_list = request.form.getlist('input_tags')
            for tag in tag_list:
                post_tag = PostTag(post_id=post.id, tag_id=Tag.query.filter_by(name=tag).first().id)
                db.session.add(post_tag)
                db.session.commit()
            flash('Post submitted!')
            return redirect(url_for('.index'))
    return render_template('index.html', posts=page_posts, pagination=pagination, tags=all_tags)
