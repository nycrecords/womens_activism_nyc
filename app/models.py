"""
Models for women's activism nyc db
"""
import re
from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, session
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime

from .utils import InvalidResetToken


class Permission:

    """
    Permissions used for User Roles
    NO_PERMISSIONS: No permissions granted to Anonymous Users
    MODERATE_STORIES: Ability to edit/delete stories
    MODERATE_TAGS: Ability to add/delete/edit tags
    MODERATE_USERS: Ability to edit/delete User accounts
    ADMINISTER: All permissions granted
    """

    NO_PERMISSIONS = 0x00
    MODERATE_STORIES = 0x04
    MODERATE_TAGS = 0x06
    MODERATE_USERS = 0x08
    ADMINISTER = 0x80


class Role(db.Model):

    """
    Specifies the properties of a role. The roles table is used to create roles such as Administrator
    and Agency User, and Poster. The roles table is linked to users table
    Poster has no permissions
    Administrator has all permissions
    """

    @staticmethod
    def insert_roles():
        roles = {
            'Poster': (Permission.NO_PERMISSIONS, False),

            'Agency_User': (
                     Permission.MODERATE_STORIES |
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


class Story(db.Model):

    """
    Specifies the properties of a story.
    activist_first is the activist's first name
    activist_last is the activist's last name
    activist_start is the birth year of the activist
    activist_end is the death year of the activist or "Today" is the activist is still alive
    activist_url is an optional link to get more information about the activist
    poster_id references a user with the Poster role
    content is the text of the story
    is_edited determines if the story has been edited by an agency user/admin
    if edited = True, pull from Post_Edit instead
    is_visible determines if the story is visible to the public
    if visible = False, a post is "deleted" (hidden from anonymous users)
    version specifies what version of the post is displaying
    """

    __tablename__ = "stories"
    id = db.Column(db.Integer, primary_key=True)
    activist_first = db.Column(db.String(30))
    activist_last = db.Column(db.String(30))
    activist_start = db.Column(db.String(4))
    activist_end = db.Column(db.String(5))
    activist_url = db.Column(db.Text)
    poster_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    content = db.Column(db.Text, nullable=False)
    creation_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    edit_time = db.Column(db.DateTime)
    is_edited = db.Column(db.Boolean, nullable=False)
    is_visible = db.Column(db.Boolean, nullable=False)
    version = db.Column(db.Integer, default=1)

    def __repr__(self):
        return '<Story %r>' % self.activist_first

    # @staticmethod
    # def generate_fake(count=100):
    #     from random import seed, randint
    #     import forgery_py
    #
    #     seed()
    #     for i in range(count):
    #         s = Story(title=forgery_py.lorem_ipsum.sentence(),
    #                  content=forgery_py.lorem_ipsum.sentences(randint(1, 5)),
    #                  creation_time=forgery_py.date.date(True),
    #                  is_edited=False,
    #                  is_visible=True)
    #         db.session.add(s)
    #         db.session.commit()


class Tag(db.Model):

    """
    Specifies the properties of a tag, "name" will be the name of the tag
    This table will be a list of our predefined tags.
    """

    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)

    def __repr__(self):
        return '<Tag %r>' % self.name


class StoryTag(db.Model):

    """
    Specifies what tags are assigned to what story
    story_id and tag_id are combined to make a unique primary key
    One story can have many tags.
    """

    __tablename__ = "story_tags"
    story_id = db.Column(db.Integer, db.ForeignKey("stories.id"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)

    def __repr__(self):
        return '<StoryTag %r>' % self.story_id


class User(UserMixin, db.Model):

    """
    Specifies the properties of a user. The role_id attribute is a foreign key to the roles table
    A user will use their email to log in
    phone should be put in with no dashes "-" in between
    phone number treated as a string in so no leading 0's are lost
    password is a hashed value
    confirmed determines if the user account is confirmed or not
    site is a poster's personal website if they want to share
    is_subscribed is a boolean to determine if a poster is added to the mailing list
    """

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(128), nullable=True)
    first_name = db.Column(db.String(30), nullable=True)
    last_name = db.Column(db.String(30), nullable=True)
    email = db.Column(db.String(50), nullable=True, index=True)
    phone = db.Column(db.String(11), nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    confirmed = db.Column(db.Boolean, default=False)
    site = db.Column(db.String(50), nullable=True)
    is_subscribed = db.Column(db.Boolean, default=False)
    login_attempts = db.Column(db.Integer, default=0)
    old_passwords = db.Column(db.Integer, db.ForeignKey('passwords.id'))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['WOMENS_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
                #self.confirmed = True
        if self.role is None:
            self.role = Role.query.filter_by(default=True).first()
        self.password_list = Password(p1='', p2='', p3='', p4='', p5='', last_changed=datetime.now())

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
        #session['reset_token'] = {'token': s, 'valid': True}
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
        # checks if the new password is at least 8 characters with at least 1 UPPERCASE AND 1 NUMBER
        # if not re.match(r'^(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z\d]{8,128}$', new_password):
        #     return False
        # # If the password has been changed within the last second, the token is invalid.
        # if (datetime.now() - self.password_list.last_changed).seconds < 1:
        #     current_app.logger.error('User {} tried to re-use a token.'.format(self.email))
        #     raise InvalidResetToken
        # self.password = new_password
        # self.password_list.update(self.password_hash)
        # db.session.add(self)
        # return True

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def __repr__(self):
        return '<User %r>' % self.first_name


class Password(db.Model):
    __tablename__ = 'passwords'
    id = db.Column(db.Integer, primary_key=True)
    p1 = db.Column(db.String(128))
    p2 = db.Column(db.String(128))
    p3 = db.Column(db.String(128))
    p4 = db.Column(db.String(128))
    p5 = db.Column(db.String(128))
    last_changed = db.Column(db.DateTime)
    users = db.relationship('User', backref='password_list', lazy='dynamic')

    def update(self, password_hash):
        self.p5 = self.p4
        self.p4 = self.p3
        self.p3 = self.p2
        self.p2 = self.p1
        self.p1 = password_hash
        self.last_changed = datetime.now()


class StoryEdit(db.Model):

    """
    Specifies properties of an edited story. Rows stored in this table are old versions of a story that have been edited
    story_id keeps track of the original story id
    user_id keeps track of the use account that make the edit
    creation_time is the original creation time of the story
    edit_time is the time that the story was edited
    type specifies is the the story was "edited" or "deleted"
    Users that make an edit must provide a reason for their actions
    """

    __tablename__ = "story_edits"
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey("stories.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    creation_time = db.Column(db.DateTime)
    edit_time = db.Column(db.DateTime)
    type = db.Column(db.String(6), nullable=False)
    activist_first = db.Column(db.String(30))
    activist_last = db.Column(db.String(30))
    activist_start = db.Column(db.String(4))
    activist_end = db.Column(db.String(5))
    activist_url = db.Column(db.Text)
    poster_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    content = db.Column(db.Text, nullable=False)
    reason = db.Column(db.Text, nullable=False)
    version = db.Column(db.Integer, default=1)

    def __repr__(self):
        return '<Edit %r>' % self.id


class Flag(db.Model):

    """
    Specifies the properties of a flag. Keeps track of the post_id of the flagged story.
    One story can have many flags. The type of flag must be specified
    when flagging a post (offensive language, wrong info,...)
    An explanation of why you want to flag a story can be included in the reason attribute
    """

    __tablename__ = "flags"
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey("stories.id"))
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


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))