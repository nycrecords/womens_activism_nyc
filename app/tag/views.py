"""
View functions for story functionality
"""
from flask import render_template, request, flash, jsonify
from flask_login import current_user, login_required

from app import db
from app.models import Events, Stories, Tags
from app.constants import event_type
from app.db_utils import create_object, update_object
from app.tag import tag


@tag.route('/edit_tags', methods=['GET', 'POST'])
@login_required
def edit_tags():
    """
    This view function is used for modifying/editing tags.
    Tags can be edited, added, or removed.

    :return: renders the 'edit_tags.html' template with the list of tags
    """
    tags = Tags.query.order_by(Tags.name).all()
    return render_template('tag/edit_tags.html', tags=tags)


@tag.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    tag_id = request.form['id']
    name = request.form['name']
    action = request.form['action']

    if action == "edit":
        tag_obj = Tags.query.filter_by(id=tag_id).one()
        prev_name = tag_obj.name
        update_object({'name': name}, Tags, tag_id)

        create_object(Events(_type=event_type.TAG_EDITED,
                             user_guid=current_user.guid,
                             previous_value=prev_name,
                             new_value=tag_obj.name))

        for story in Stories.query.filter(Stories.tags.any(prev_name)).all():
            prev_story_tags = story.tags
            new_story_tags = [tag_obj.name if t == prev_name else t for t in prev_story_tags]
            update_object({'tags': new_story_tags}, Stories, story.id)

            create_object(Events(
                _type=event_type.EDIT_STORY,
                story_id=story.id,
                previous_value={'tags': prev_story_tags},
                new_value={'tags': new_story_tags}
            ))

        flash('Tag is edited successfully!', category='success')
    # TODO: implement elasticsearch changes
    # elif action == "remove":
    #     db.session.delete(tag_obj)
    #     db.session.commit()
    #
    #     event = Events(_type=event_type.TAG_DELETED,
    #                    user_guid=current_user.guid,
    #                    previous_value=tag_obj)
    #     create_object(event)
    #
    #     flash('Tag is removed successfully!', category='success')
    else:
        new_name = request.form['name']
        tag_obj = Tags.query.filter_by(name=new_name).one_or_none()
        if not tag_obj:
            new_tag = create_object(Tags(name=new_name))

            event = Events(_type=event_type.TAG_CREATED,
                           user_guid=current_user.guid,
                           new_value=new_tag)
            create_object(event)

            flash("Tag is added successfully!", category='success')
        else:
            flash("Tag already exists!", category='warning')

    return jsonify({'result': 'success'})
