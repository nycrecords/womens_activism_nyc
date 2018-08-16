"""
View functions for story functionality
"""
from flask import render_template, request, flash, jsonify
from flask_login import login_required

from app import db
from app.models import Tags
from app.tag import tag
from app.db_utils import create_object, update_object
from operator import attrgetter


@tag.route('/edit_tags', methods=['GET', 'POST'])
@login_required
def edit_tags():
    tags = sorted(Tags.query.all(), key=attrgetter('id'))

    return render_template('tag/edit_tags.html', tags=tags)


@tag.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    tag_id = request.form['id']
    name = request.form['name']
    action = request.form['action']

    if action == "edit":
        update_object({'name': name}, Tags, tag_id)
        flash('Tag is edited successfully!', category='success')
    elif action == "remove":
        tag = Tags.query.get(tag_id)
        db.session.delete(tag)
        db.session.commit()
        flash('Tag is removed successfully!', category='success')
    else:
        new_name = request.form['name']
        create_object(Tags(name=new_name))
        flash('Tag is added successfully!', category='success')

    return jsonify({'result': 'success'})
