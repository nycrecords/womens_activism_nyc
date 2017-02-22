from flask import render_template, redirect, url_for, flash
from app import db
from app.models import Tag, PostTag
from app.tags.forms import AddTagForm, RemoveTagForm, EditTagForm
from app.tags import tags
from flask_login import login_required
from app.db_helpers import put_obj, delete_obj


#  TODO: DOCSTRINGS


@tags.route('/tags', methods=['GET', 'POST'])
@login_required
def tags():
    tags = Tag.query.all()
    addform = AddTagForm()
    removeform = RemoveTagForm()
    editform = EditTagForm()
    add = addform.add.data
    delete = removeform.remove.data
    current = editform.current.data
    edit = editform.edit.data
    if addform.validate_on_submit():
        if len(add) > 0:  # Checks if add field exists
            add = add.strip()
            if len(add) == 0:  # Checks if add field is whitespace
                flash("Tag cannot be whitespace.")
                return redirect(url_for('.tags', addform=addform, removeform=removeform, editform=editform, tags=tags))
            if Tag.query.filter_by(name=add).first():  # Checks if tag in add field exists in database
                flash('Tag already in the list.')
                return render_template('tags/tags.html', addform=addform, removeform=removeform, editform=editform, tags=tags)
            else:
                add_tag = Tag(name=add)
                put_obj(add_tag)
                flash('New tag had been added.')
            return redirect(url_for('.tags', addform=addform, removeform=removeform, editform=editform, tags=tags))
    if removeform.validate_on_submit():
        if len(delete) > 0:  # Checks if delete field exists
            delete = delete.strip()
            if not Tag.query.filter_by(name=delete).first():  # Checks if tag in delete field exists in database
                flash("Tag doesn't exist.")
                return render_template('tags/tags.html', addform=addform, removeform=removeform, editform=editform, tags=tags)
            else:
                post_tags = PostTag.query.filter_by(tag_id=Tag.query.filter_by(name=delete).first().id).all()
                for post_tag in post_tags:
                    delete_obj(post_tag)
                delete_tag = Tag.query.filter_by(name=delete).first()
                delete_obj(delete_tag)
                flash('The tag has been deleted.')
            return redirect(url_for('.tags'))
    if editform.validate_on_submit():
        if len(current) > 0 and len(edit) == 0:  # Checks if edit field is empty when current field is not
            flash("Edit field is empty.")
            return render_template('tags/tags.html', addform=addform, removeform=removeform, editform=editform, tags=tags)
        if len(current) == 0 and len(edit) > 0:  # Checks if current field is empty when edit field is not
            flash("Please enter a tag to edit.")
            return render_template('tags/tags.html', addform=addform, removeform=removeform, editform=editform, tags=tags)
        if len(current) > 0 and len(edit) > 0:  # Checks if both edit field and current field exist
            current = current.strip()
            edit = edit.strip()
            if not Tag.query.filter_by(name=current).first():  # Checks if tag in current field exists
                flash("Please enter an existing tag.")
                return render_template('tags/tags.html', addform=addform, removeform=removeform, editform=editform, tags=tags)
            else:
                if len(edit) == 0:  # Checks if edit field is whitespace
                    flash("Edit field cannot have whitespace.")
                    return redirect(url_for('.tags', addform=addform, removeform=removeform, editform=editform, tags=tags))
                if Tag.query.filter_by(name=edit).first():  # Checks if tag in edit field is in database
                    flash("Tag already exists.")
                    return render_template('tags/tags.html', addform=addform, removeform=removeform, editform=editform, tags=tags)
                else:
                    current_tag = Tag.query.filter_by(name=current).first()
                    current_tag.name = edit
                    db.session.commit()
                    flash('Tag was successfully changed.')
            return redirect(url_for('.tags', addform=addform, removeform=removeform, editform=editform, tags=tags))
    return render_template('tags/tags.html', addform=addform, removeform=removeform, editform=editform, tags=tags)