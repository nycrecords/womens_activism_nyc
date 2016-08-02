from flask import render_template, request, current_app
from .. import db
from ..models import Post
from . import posts


@posts.route('/posts', methods=['GET', 'POST'])
def all_posts():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.creation_time.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=True)
    posts=pagination.items
    return render_template('postsTab.html', posts=posts, pagination=pagination)


@posts.route('/posts/<int:id>', methods=['GET', 'POST'])
def posts(id):
    post = Post.query.get_or_404(id)
    title = post.title
    content = post.content
    content_html = post.content_html
    creation_time = post.creation_time
    is_edited = post.is_edited
    #return render_template('post.html', title=title, content=content, content_html=content_html,
    #                       creation_time=creation_time, is_edited=is_edited)
    return render_template('post.html', post=post)


#{ % if post.content_html %}
#{{post.content_html | safe}}
#{ % else %}
#{{post.content}}
#{ % endif %}

