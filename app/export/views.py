from flask import render_template, request

from flask_login import login_required
from app.export import export
from app.export.forms import ExportForm
import csv
from io import StringIO, BytesIO
from app.models import Users
from flask.helpers import send_file


@export.route('/', methods=['GET','POST'])
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
                    attachment_filename="Subscribers.csv",
                    as_attachment=True
                )
            return '', 400
    return render_template('export/export.html', form=form)