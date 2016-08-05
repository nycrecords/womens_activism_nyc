"""
Models for women's activism nyc db
"""

from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from datetime import datetime, timedelta


class Permission:
    MODERATE_COMMENTS = 0x02
    MODERATE_POST = 0x04
    MODERATE_TAGS = 0x06
    MODERATE_USERS = 0x08
    ADMINISTER = 0x80


class Role(db.Model):

    """
    Specifies the properties of a role. The roles table is used to create roles such as Administrator
    and Agency Use. The roles table is linked to users table
    """

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.MODERATE_COMMENTS |
                          Permission.MODERATE_POST |
                          Permission.MODERATE_TAGS, True),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


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
    content = db.Column(db.Text, nullable=False)
    creation_time = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    is_edited = db.Column(db.Boolean, nullable=False)
    is_visible = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return '<Post %r>' % self.title

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py

        seed()
        for i in range(count):
            p = Post(title=forgery_py.lorem_ipsum.sentence(),
                     content=forgery_py.lorem_ipsum.sentences(randint(1, 5)),
                     creation_time=forgery_py.date.date(True),
                     is_edited=False,
                     is_visible=True)
            db.session.add(p)
            db.session.commit()

    def just_now(self):
        a = datetime.utcnow()
        b = self.creation_time
        difference = a - b
        difference_in_minutes = difference / timedelta(minutes=1)
        if difference_in_minutes < 5:
            return True
        return False


class Tag(db.Model):

    """
    Specifies the properties of a tag, "name" will be the name of the tag
    This table will be a list of our predefined tags.
    """

    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)

    def __repr__(self):
        return '<Tag %r>' % self


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
    edit_time = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    type = db.Column(db.Enum('Edit', 'Delete', name='comment_edit_types'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    reason = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Edit %r>' % self.id


class User(UserMixin, db.Model):

    """
    Specifies the properties of a user. The role attribute is a foreign key to the roles table
    The role attribute should either be "agency user" or "admin"
    A user's email address must be unique
    A user will use their email to log in
    phone should be put in with no dashes "-" in between
    phone number treated as a string in so no leading 0's are lost
    password is a hashed value
    confirmed determines if the user account is confirmed or not
    """

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True, index=True)
    phone = db.Column(db.String(11), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    confirmed = db.Column(db.Boolean, default=False)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['WOMENS_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            else:
                self.role = Role.query.filter_by(default=True).first()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

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
    edit_time = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
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
    type = db.Column(db.String(30))
    reason = db.Column(db.String(500), nullable=False)

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
    reason = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return '<Feedback %r>' % self.title


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
