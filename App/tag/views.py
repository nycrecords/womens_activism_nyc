from flask import render_template, redirect, url_for, current_app, flash
from .. import db
from ..models import *
from ..email import send_email
from .forms import TagForm
from . import tags

from flask_login import login_required


@login_required
@tags.route('/tags', methods=['GET', 'POST'])
def tags():
    tags = Tag.query.all()
    form = TagForm()
    add = form.add.data
    delete = form.remove.data
    if form.validate_on_submit():
        if len(add) > 0:
            add_tag = Tag(name=add)
            db.session.add(add_tag)
            db.session.commit()
            flash('New tag had been added.')
        if len(delete) > 0:
            delete_tag = Tag.query.filter_by(name=delete).first()
            print(delete_tag)
            db.session.delete(delete_tag)
            db.session.commit()
            flash('The tag had been deleted.')
        return redirect(url_for('.tags', form=form, tags=tags))
    return render_template('tags.html', form=form, tags=tags)