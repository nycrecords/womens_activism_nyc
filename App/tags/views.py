from flask import render_template, redirect, url_for, flash
from .. import db
from ..models import Tag
from .forms import AddTagForm, RemoveTagForm, EditTagForm
from . import tags
from flask_login import login_required
@login_required
@tags.route('/tags', methods=['GET', 'POST'])
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
                return render_template('tags.html', addform=addform, removeform=removeform, editform=editform, tags=tags)
            else:
                add_tag = Tag(name=add)
                db.session.add(add_tag)
                db.session.commit()
                flash('New tag had been added.')
            return redirect(url_for('.tags', addform=addform, removeform=removeform, editform=editform, tags=tags))
    if removeform.validate_on_submit():
        if len(delete) > 0:  # Checks if delete field exists
            delete = delete.strip()
            if not Tag.query.filter_by(name=delete).first():  # Checks if tag in delete field exists in database
                flash("Tag doesn't exist.")
                return render_template('tags.html', addform=addform, removeform=removeform, editform=editform, tags=tags)
            else:
                delete_tag = Tag.query.filter_by(name=delete).first()
                db.session.delete(delete_tag)
                db.session.commit()
                flash('The tag has been deleted.')
            return redirect(url_for('.tags'))
    if editform.validate_on_submit():
        if len(current) > 0 and len(edit) == 0:  # Checks if edit field is empty when current field is not
            flash("Edit field is empty.")
            return render_template('tags.html', addform=addform, removeform=removeform, editform=editform, tags=tags)
        if len(current) == 0 and len(edit) > 0:  # Checks if current field is empty when edit field is not
            flash("Please enter a tag to edit.")
            return render_template('tags.html', addform=addform, removeform=removeform, editform=editform, tags=tags)
        if len(current) > 0 and len(edit) > 0:  # Checks if both edit field and current field exist
            current = current.strip()
            edit = edit.strip()
            if not Tag.query.filter_by(name=current).first():  # Checks if tag in current field exists
                flash("Please enter an existing tag.")
                return render_template('tags.html', addform=addform, removeform=removeform, editform=editform, tags=tags)
            else:
                if len(edit) == 0:  # Checks if edit field is whitespace
                    flash("Edit field cannot have whitespace.")
                    return redirect(url_for('.tags', addform=addform, removeform=removeform, editform=editform, tags=tags))
                if Tag.query.filter_by(name=edit).first():  # Checks if tag in edit field is in database
                    flash("Tag already exists.")
                    return render_template('tags.html', addform=addform, removeform=removeform, editform=editform, tags=tags)
                else:
                    current_tag = Tag.query.filter_by(name=current).first()
                    current_tag.name = edit
                    db.session.commit()
                    flash('Tag was successfully changed.')
            return redirect(url_for('.tags', addform=addform, removeform=removeform, editform=editform, tags=tags))
    return render_template('tags.html', addform=addform, removeform=removeform, editform=editform, tags=tags)