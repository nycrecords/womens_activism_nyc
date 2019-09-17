from flask import (
    render_template,
    flash,
    request,
    Markup,
    current_app,
    redirect,
    url_for,
)

from app.unsubscribe import unsubscribe
from app.unsubscribe.forms import UnsubscribeForm
from app.edit.utils import update_user
from app.models import Users, Events
from app.lib.emails_utils import send_email
from app.constants.event import EMAIL_SENT
from app.db_utils import create_object


@unsubscribe.route("/", methods=["GET", "POST"])
def unsubscribe():
    form = UnsubscribeForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            if form.user_email.data:
                user = Users.query.filter_by(
                    email=form.user_email.data, subscription=True
                ).one_or_none()
                if user is not None:
                    user_guid = update_user(
                        user,
                        user.first_name,
                        user.last_name,
                        form.user_email.data,
                        user.phone,
                        False,
                    )
                    email_body = render_template(
                        "emails/remove_subscriber_agency.html",
                        first_name=user.first_name,
                        last_name=user.last_name,
                        email=form.user_email.data,
                        phone=user.phone,
                    )
                    send_email(
                        subject="WomensActivism - Remove Subscriber",
                        sender=current_app.config["MAIL_SENDER"],
                        recipients=[current_app.config["MAIL_RECIPIENTS"]],
                        html_body=email_body,
                    )
                    create_object(
                        Events(
                            _type=EMAIL_SENT,
                            user_guid=user_guid,
                            new_value={"email_body": email_body},
                        )
                    )
                    flash(Markup("You are no longer subscribed."), category="success")
                else:
                    flash("No subscription found.", category="warning")
                return redirect(url_for("unsubscribe.unsubscribe"))
    else:
        return render_template("unsubscribe/unsubscribe.html", form=form)
