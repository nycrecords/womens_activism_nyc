import csv
from datetime import datetime

from flask import render_template, request, flash, redirect, url_for
from flask.helpers import send_file
from flask_login import login_required
from io import StringIO, BytesIO

from app.export import export
from app.export.forms import ExportForm
from app.models import Users


@export.route('/', methods=['GET', 'POST'])
@login_required
def export():
    form = ExportForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            users = Users.query.filter_by(subscription=True).all()
            if users:
                buffer = StringIO()
                writer = csv.writer(buffer)
                writer.writerow(["First Name",
                                 "Last Name",
                                 "Email",
                                 "Phone Number"])
                for users in users:
                    writer.writerow([users.first_name or '',
                                     users.last_name or '',
                                     users.email or '',
                                     users.phone or ''])

                return send_file(
                    BytesIO(buffer.getvalue().encode('UTF-8')),
                    attachment_filename="subscribers_{}.csv".format(
                        datetime.now().strftime("%Y_%m_%d_at_%I_%M_%p")),
                    as_attachment=True
                )
            else:
                flash("No subscribers found.", category='warning')
                return redirect(url_for('export.export'))
    return render_template('export/export.html', form=form)
