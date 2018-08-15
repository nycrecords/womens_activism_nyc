"""
View functions for story functionality
"""
from flask import render_template, request, jsonify
from flask_login import login_required

from app.models import Tags
from app.tag import tag


@tag.route('/edit_tags', methods=['GET', 'POST'])
@login_required
def edit_tags():
    tags = Tags.query.all()

    return render_template('tag/edit_tags.html', tags=tags)


@tag.route('/update', methods=['POST'])
@login_required
def update():
        print('hello')
        tag_id = request.form['id']
        name = request.form['name']
        print(tag_id, name)
        return jsonify({'result': 'success'})
