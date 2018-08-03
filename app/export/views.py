from flask import render_template, request, flash, redirect, url_for, Markup, current_app
from flask_login import login_required
from app.export import export
from app.export.forms import ExportForm
import csv
from io import StringIO, BytesIO
from app.models import Users


@export.route('/', methods=['GET','POST'])
@login_required
def export():
    form = ExportForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            users = Users.query.filter_by(subscription=True).all()
            if users:
                buffer = StringIO()  # csvwriter cannot accept BytesIO
                writer = csv.writer(buffer)
                writer.writerow(["First Name",
                                 "Last Name",
                                 "Email",
                                 "Phone Number"])
                writer.writerow([users.first_name or '',
                                 users.last_name or '',
                                 users.email or '',
                                 users.phone or ''])

                return export(
                    BytesIO(buffer.getvalue().encode('UTF-8')),  # convert to bytes
                    attachment_filename="subscribers.csv",
                    as_attachment=True
                )
            return '', 400
            
            #flash(Markup('Now exporting!'), category='success')

    return render_template('export/export.html', form=form)