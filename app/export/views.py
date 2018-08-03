from flask import render_template, request, flash, redirect, url_for,Markup
from flask_login import login_required
from app.export import export
from app.export.forms import ExportForm
import io
import csv
from flask import make_response
from app.models import Users


@export.route('/', methods=['GET','POST'])
@login_required
def export():
    form = ExportForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = Users.query.filter_by(first_name=form.user_first.data,
                                         last_name=form.user_last.data,
                                         email=form.user_email.data,
                                         phone=form.user_phone.data,
                                         subscription=True).one_or_none()
            si = io.BytesIO()
            cw = csv.writer(si, dialect='excel')
            cw.writerows(user)
            output = make_response(si.getvalue())
            output.headers["Content-Disposition"] = "attachment; filename=export.csv"
            output.headers["Content-type"] = "text/csv"
            flash(Markup('Now exporting!'), category='success')
            return output
    return render_template('export/export.html', form=form)