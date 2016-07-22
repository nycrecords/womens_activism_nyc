"""
Models for women's activism nyc db
"""

from flask import Flask, render_template, redirect, url_for
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Shell
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://@localhost/women'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


class FeedbackForm(Form):
    subject = StringField('What is the subject', validators=[DataRequired("Please enter the subject")])
    email = StringField('What is your email?', validators=[DataRequired("Please enter your email")])
    reason = TextAreaField('Reason for report?', validators=[DataRequired("Please enter your report")])
    submit = SubmitField('Submit')



class Post(db.Model):

    """
    Specifies the properties of a post. A post will show the title, content, and creation time to anonymous users.
    is_edited determines if the post has been edited by an agency user/admin
    if edited = True, pull from Post_Edit instead
    is_visible determines if the post is visible to the public
    if visible = False, a post is "deleted" (hidden from anonymous users)
    """

    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    content = db.Column(db.String(5000), nullable=False)
    creation_time = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    is_edited = db.Column(db.Boolean, nullable=False)
    is_visible = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return '<Post %r>' % self.title


class Tag(db.Model):

    """
    Specifies the properties of a tag, "name" will be the name of the tag
    This table will be a list of our predefined tags.
    """

    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    #test = db.Column(db.Enum('test1', 'test2', name='types'), nullable=True)

    #type = db.Column(db.Enum('Offensive language', 'Wrong information', 'Inappropriate content', name='flag_types'))

    def __repr__(self):
        return '<Tag %r>' % self.name


class PostTag(db.Model):

    """
    Specifies what tags are assigned to what posts, post_id and tag_id are
    combined to make a unique primary key. One post can have many tags.
    """

    __tablename__ = "post_tags"
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)

    def __repr__(self):
        return '<Post_Tag %r>' % self.post_id


class Comment(db.Model):

    """
    Specifies the properties of a comment. A comment is assigned to an existing post referenced by post_id
    Comments only show the content and time. One post can have many comments.
    if is_edited = True then an agency user/admin has edited the comment
    if is_visible = False then an agency user/admin has "deleted" the comment (made it hidden to the public)
    """

    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    content = db.Column(db.String(750), nullable=False)
    creation_time = db.Column(db.DateTime,  nullable=False)
    is_edited = db.Column(db.Boolean, nullable=False)
    is_visible = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return '<Comment %r>' % self.id


class CommentEdit(db.Model):

    """
    Specifies properties of an edited comment. An edited post keeps track of the original comment.id,
    the user.id of who edited the comment, the time it was edited,
    the type of edit that was made (an edit or a deletion),
    the contents of the newly edited comment, and reason why the user edited the comment.
    If there were multiple edits made to a comment, pull the most recent change based off edit_time
    """

    __tablename__ = "comment_edits"
    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey("comments.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    edit_time = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.Enum('Edit','Delete', name='comment_edit_types'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    reason = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Edit %r>' % self.id


class User(db.Model):

    """
    Specifies the properties of a user. The role attribute should either be "agency user" or "admin"
    A user's email address must be unique
    A user will use their email to log in
    phone should be put in with no dashes "-" in between
    phone number treated as a string in so no leading 0's are lost
    password should be hashed
    """

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(20), nullable=False)  # need to hash the password
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    phone = db.Column(db.String(11), nullable=False)
    #role = db.Column(db.String(20), nullable=False)
    role = db.Column(db.Enum('Administrator', 'Agency User', name='user_roles'), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.first_name


class PostEdit(db.Model):

    """
    Specifies properties of an edited post. An edited post keeps track of the original post.id,
    the user_id of who edited the post, the time it was edited, the type of edit that was made (an edit or a deletion),
    the contents of the newly edited post, and reason why the user edited the post.
    If there were multiple edits made to a post, pull the most recent change based off edit_time
    """

    __tablename__ = "post_edits"
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    edit_time = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(6), nullable=False)
    content = db.Column(db.Text, nullable=False)
    reason = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Edit %r>' % self.id


class Flag(db.Model):

    """
    Specifies the properties of a flag. Keeps track of the post_id of the flagged post.
    One post can have many flags. The type of flag must be specified
    when flagging a post (offensive language, wrong info,...)
    An explanation of why you want to flag a post can be included in the reason attribute
    """

    __tablename__ = "flags"
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))
    # type = db.Column(db.String(30), nullable=False)  # make this an enum
    type = db.Column(db.Enum(
        'Offensive content', 'Wrong information', 'Inappropriate content', 'Other ', name='flag_types'))
    reason = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Flag %r>' % self.id


class Feedback(db.Model):

    """
    Specifies properties of a feedback form. A title must be included and reason must be included,
    email will be hidden and optional.
    """

    __tablename__ = "feedback"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=True)
    reason = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Feedback %r>' % self.title


def make_shell_context():
    return dict(app=app, db=db, Post=Post, Tag=Tag, Post_Tag=PostTag,
                Comment=Comment, CommentEdit=CommentEdit, User=User, Post_Edit=PostEdit, Flag=Flag, Feedback=Feedback)

manager.add_command("shell", Shell(make_context=make_shell_context))


@app.route('/', methods=['GET', 'POST'])
def index():
    title = None
    reason = None
    comment = None
    form = FeedbackForm()

    if form.validate_on_submit():
        subject = form.subject.data
        email = form.email.data
        reason = form.reason.data
        print('Subject: {}\nEmail: {}\nReason: {}'.format(subject, email, reason))

        feedback = Feedback(title = subject, email = email, reason = reason)
        db.session.add(feedback)
        session=['known']
        #return render_template('index.html', form=form)
        return redirect(url_for('index'))

    return render_template('index.html', form=form)



if __name__ == '__main__':
    manager.run()