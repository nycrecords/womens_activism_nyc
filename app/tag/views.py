"""
View functions for story functionality
"""
from flask import render_template, request, flash, redirect, url_for, jsonify
from flask_login import current_user, login_required

from app import db
from app.constants.event import EDIT_FEATURED_STORY
from app.db_utils import create_object, update_object
from app.tag import tag
from app.models import Events, FeaturedStories, Stories, Tags
from operator import attrgetter

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