import csv
from datetime import datetime

from flask import render_template, request, flash, redirect, url_for, Markup
from flask.helpers import send_file
from flask_login import login_required
from io import StringIO, BytesIO
from sqlalchemy import or_

from app.export import export
from app.export.forms import ExportForm
from app.models import Subscribers


@export.route('/', methods=['GET', 'POST'])
@login_required
def export():
    form = ExportForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            subscribers = Subscribers.query.filter(
                or_(Subscribers.email.isnot(None), Subscribers.phone.isnot(None))).all()
            if subscribers:
                buffer = StringIO()
                writer = csv.writer(buffer)
                writer.writerow(["First Name",
                                 "Last Name",
                                 "Email",
                                 "Phone Number"])
                for s in subscribers:
                    writer.writerow([Markup(s.first_name).unescape() or '',
                                     Markup(s.last_name).unescape() or '',
                                     Markup(s.email).unescape() or '',
                                     Markup(s.phone).unescape() or ''])

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
