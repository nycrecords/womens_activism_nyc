"""
Models for women's activism nyc db
"""

import os
from flask import Flask, render_template
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Shell

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://@localhost/womens_activism_nyc'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

manager = Manager(app)
db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


class Post(db.Model):

    """
    Specifies the properties of a post. A post will show the title, content, and time.
    if edited = True, pull from Post_Edit instead
    if visible = False, a post is "deleted"
    """

    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    content = db.Column(db.Text, nullable=False)
    time = db.Column(db.DateTime, nullable=True)
    edited = db.Column(db.Boolean, nullable=True)
    visible = db.Column(db.Boolean, nullable=True)

    def __repr__(self):
        return '<Post %r>' % self.title


class Tag(db.Model):

    """
    Specifies the properties of a tag. A tag will have a tag name.
    This table will be a list of predefined tags.
    """

    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, index=True)


    def __repr__(self):
        return '<Tag %r>' % self.name


class Post_Tag(db.Model):

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
    Specifies the properties of a comment. A comment is assigned to an existing post_id
    Comments only show the content and time. One post can have many comments.
    """

    __tablename__ = "comments"
    comment_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    content = db.Column(db.Text, nullable=False, index=True)
    time = db.Column(db.DateTime,  nullable=True)


    def __repr__(self):
        return '<Comment %r>' % self.comment_id



class User(db.Model):

    """
    Specifies the properties of a user. A user can be either an admin or agency user.
    A user's email address must be unique
    """

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String(20), nullable=False)
    last = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String (30), nullable=False, unique=True)
    phone = db.Column(db.String(10), nullable=False)
    role = db.Column(db.String(10), nullable=False)


    def __repr__(self):
        return '<User %r>' % self.first



class Post_Edit(db.Model):

    """
    Specifies properties of an edited post. An edited post keeps track of the original post_id,
    the user_id of who edited the post, the time it was edited, the type of edit that was made (an edit of a deletion),
    the contents of the newly edited post, and the reason why the user edited the post.
    If there were multiple edits made to a post, pull the most recent change based off time
    """

    __tablename__ = "post_edits"
    edit_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    time = db.Column(db.DateTime, nullable=True)
    type = db.Column(db.String(6), nullable=False)
    content = db.Column(db.Text, nullable=False)
    reason = db.Column(db.Text, nullable=False)


    def __repr__(self):
        return '<Edit %r>' % self.edit_id


class Flag(db.Model):

    """
    Specifies the properties of a flag. Keeps track of the post_id of the flagged post.
    One post can have many flags. The type of flag must be specified
    when flaggin a post (offensive langugae, wrong info,...)
    An explanation of why you want to flag a must be included in the reason attribute
    """

    __tablename__ = "flags"
    flag_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))
    type = db.Column(db.String(30), nullable=False)
    reason = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Flag %r>' % self.flag_id


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
    return dict(app=app, db=db, Post=Post, Tag=Tag, Post_Tag=Post_Tag,
                Comment=Comment, User=User, Post_Edit=Post_Edit, Flag=Flag, Feedback=Feedback)

manager.add_command("shell", Shell(make_context=make_shell_context))


if __name__ == '__main__':
    manager.run()