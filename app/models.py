from app import db, es
from app.constants import (
    permission,
    role_name,
    tag,
    user_type_auth,
    event_type,
    module,
    flag
)
from app.constants.search import ES_DATETIME_FORMAT

from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON, ARRAY

from . import login_manager
from werkzeug.security import generate_password_hash, check_password_hash


class Roles(db.Model):
    """
    Define the Roles class with the following columns:

    id - an integer containing the role id
    name - a string containing the name of the role
    permission - a string containing the number value for permissions of a role
    """
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    permissions = db.Column(db.Integer)

    @classmethod
    def populate(cls):
        """
        Insert permissions for each role.
        """

        roles = {
            role_name.ANONYMOUS: (
                permission.NONE
            ),
            role_name.MODERATOR: (
                    permission.EDIT_STORY |
                    permission.DELETE_STORY |
                    permission.EDIT_COMMENT |
                    permission.DELETE_COMMENT |
                    permission.EDIT_FEATURED_STORY |
                    permission.EDIT_THEN_AND_NOW |
                    permission.EDIT_EVENTS
            ),
            role_name.ADMINISTRATOR: (
                    permission.EDIT_STORY |
                    permission.DELETE_STORY |
                    permission.EDIT_COMMENT |
                    permission.DELETE_COMMENT |
                    permission.EDIT_FEATURED_STORY |
                    permission.EDIT_THEN_AND_NOW |
                    permission.EDIT_EVENTS |
                    permission.CREATE_USER |
                    permission.EDIT_USER_INFO |
                    permission.DELETE_USER
            )
        }

        for name, value in roles.items():
            role = Roles.query.filter_by(name=name).first()
            if role is None:
                role = cls(name=name)
            role.permissions = value
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Roles %r>' % self.name


class Users(UserMixin, db.Model):
    """
    Define the User class with the following columns and relationships:

    guid - an integer that contains the guid of a user, part of a composite primary key
    auth_user_type - an integer that contains that authentication type of a user, part of a composite primary key
    is_mod - a boolean that determines if a user is a moderator or not
    is_admin - a boolean that determines if a user is an admin or not
    first_name - a string that contains the first name of the user
    middle_initial - a string the contains the middle initial of the user
    last_name - a string that contains the last name of the user
    email - a string that contains the email of the user
    password_hash - a string that contains the password of the user
    """
    __tablename__ = "users"
    guid = db.Column(db.String(64), primary_key=True)
    auth_user_type = db.Column(
        db.Enum(user_type_auth.AGENCY_USER,
                user_type_auth.AGENCY_LDAP_USER,
                user_type_auth.PUBLIC_USER_FACEBOOK,
                user_type_auth.PUBLIC_USER_MICROSOFT,
                user_type_auth.PUBLIC_USER_YAHOO,
                user_type_auth.PUBLIC_USER_LINKEDIN,
                user_type_auth.PUBLIC_USER_GOOGLE,
                user_type_auth.PUBLIC_USER_NYC_ID,
                user_type_auth.ANONYMOUS_USER,
                name='auth_user_type'), nullable=False)
    is_mod = db.Column(db.Boolean, default=False, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    first_name = db.Column(db.String(300))
    middle_initial = db.Column(db.String(1))
    last_name = db.Column(db.String(300))
    email = db.Column(db.String(1024))
    email_validated = db.Column(db.Boolean, nullable=False)
    phone = db.Column(db.String(25))
    terms_of_use_accepted = db.Column(db.Boolean, nullable=False)
    password_hash = db.Column(db.String(128))

    def __init__(
            self,
            guid,
            auth_user_type,
            is_mod=False,
            is_admin=False,
            first_name=None,
            middle_initial=None,
            last_name=None,
            email=None,
            email_validated=False,
            phone=None,
            terms_of_use_accepted=False,
            password_hash=None
    ):
        self.guid = guid
        self.auth_user_type = auth_user_type
        self.is_mod = is_mod
        self.is_admin = is_admin
        self.first_name = first_name
        self.middle_initial = middle_initial
        self.last_name = last_name
        self.email = email
        self.email_validated = email_validated
        self.phone = phone
        self.terms_of_use_accepted = terms_of_use_accepted
        self.password_hash = password_hash

    @property
    def val_for_events(self):
        """
        JSON to store in Events 'new_value' field.
        """
        return {
            'guid': self.guid,
            'auth_user_type': self.auth_user_type,
            'email_validated': self.email_validated,
            'terms_of_use_accepted': self.terms_of_use_accepted
        }

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.get_id()

    def get_id(self):
        return str(self.guid)


class Anonymous(AnonymousUserMixin):
    @property
    def is_authenticated(self):
        """
        Anonymous users are not authenticated.
        :return: Boolean
        """
        return False

    @property
    def is_admin(self):
        """
        Anonymous users are treated differently from Public Users who are authenticated. This method always
        returns False.
        :return: Boolean
        """
        return False

    @property
    def is_anonymous(self):
        """
        Anonymous users always return True
        :return: Boolean
        """
        return True

    @property
    def is_moderator(self):
        """
        Anonymous users always return False
        :return: Boolean
        """
        return False


class Stories(db.Model):
    """
    Define the Stories class with the following columns and relationships:

    id - an integer containing the story id
    activist_first - a string containing the activist's first name
    activist_last - a string containing the activist's last name
    activist_start- a string containing the activist's birth year
    activist_start - an integer containing the the activist's birth year. If the activist was born in a BC year, set
    the value to negative
    activist_end - an integer containing the activist's death year. If the user wrote "Today", set this value to 9999
    content - a string containing the story about the activist
    activist_url - a string containing a link to additional information about the activist
    image_url - a string containing a link to an image of the activist
    video_url - a string containing a link to a video about the activist
    poster_id - an integer containing the id of the user who wrote the story
    date_created - a date of when the story was originally created
    is_edited - a boolean that determines if the story was edited. True = the story was edited,
                False = the story was not edited
    is_visible - a boolean that determines if the story has been hidden from the public.
                 True = the story has been hidden, False = the story has not been hidden
    tags - an array containing the tags the user selected when creating the story. The array is a string type.
    """
    __tablename__ = "stories"
    id = db.Column(db.Integer, primary_key=True)
    activist_first = db.Column(db.String(300), nullable=False)
    activist_last = db.Column(db.String(300), nullable=False)
    activist_start = db.Column(db.Integer)
    activist_end = db.Column(db.Integer)
    content = db.Column(db.Text, nullable=False)
    activist_url = db.Column(db.Text)
    image_url = db.Column(db.Text)
    video_url = db.Column(db.Text)
    user_guid = db.Column(db.String(64), db.ForeignKey("users.guid"))
    date_created = db.Column(db.DateTime, nullable=False)
    is_edited = db.Column(db.Boolean, nullable=False)
    is_visible = db.Column(db.Boolean, nullable=False)
    tags = db.Column(ARRAY(db.String(500)))

    def __init__(
            self,
            activist_first,
            activist_last,
            content,
            tags,
            is_visible=True,
            activist_start=None,
            activist_end=None,
            activist_url=None,
            image_url=None,
            video_url=None,
            user_guid=None,
            is_edited=False,
    ):
        self.activist_first = activist_first
        self.activist_last = activist_last
        self.activist_start = activist_start
        self.activist_end = activist_end
        self.content = content
        self.activist_url = activist_url
        self.image_url = image_url
        self.video_url = video_url
        self.user_guid = user_guid
        self.date_created = datetime.utcnow()
        self.is_edited = is_edited
        self.is_visible = is_visible
        self.tags = tags

    @property
    def val_for_events(self):
        """
        JSON to store in Events 'new_value' field.
        """
        return {
            'activist_first': self.activist_first,
            'activist_last': self.activist_last,
            'activist_start': self.activist_start,
            'activist_end': self.activist_end,
            'content': self.content,
            'activist_url': self.activist_url,
            'image_url': self.image_url,
            'video_url': self.video_url
        }

    def es_create(self):
        """Create elasticsearch doc"""
        es.create(
            index=current_app.config["ELASTICSEARCH_INDEX"],
            doc_type='story',
            id=self.id,
            body={
                'activist_first': self.activist_first,
                'activist_last': self.activist_last,
                'content': self.content,
                'image_url': self.image_url,
                'tag': self.tags,
                'date_created': self.date_created.strftime(ES_DATETIME_FORMAT)
            }
        )

    def es_update(self):
        es.update(
            index=current_app.config["ELASTICSEARCH_INDEX"],
            doc_type='story',
            id=self.id,
            body={
                'doc': {
                    'activist_first': self.activist_first,
                    'activist_last': self.activist_last,
                    'content': self.content,
                    'image_url': self.image_url,
                    'tag': self.tags,
                }
            }
        )

    def __repr__(self):
        return '<Stories %r>' % self.id


class FeaturedStories(db.Model):
    """
    Define the FeaturedStories class with the following columns and relationships:
    Events are used to create an audit trail of new featured story

    id - an integer that contains the featured story id
    story_id - an integer that contains the story id
    left_right - a boolean that contains whether to have picture on left OR right hand side
    timestamp - the date that the event was created
    """
    __tablename__ = "featured_stories"
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey('stories.id'), nullable=False)
    # left is true, right is false
    left_right = db.Column(
        db.Enum('left',
                'right',
                name='photo_position'), nullable=False)
    is_visible = db.Column(db.Boolean, nullable=False)
    title = db.Column(db.String(90), nullable=False)
    description = db.Column(db.String(365), nullable=False)
    rank = db.Column(db.Integer)

    story = db.relationship("Stories", backref="featured_stories")

    def __init__(
            self,
            story_id,
            title,
            description,
            left_right=False,
            is_visible=False,
            rank=None
    ):
        self.story_id = story_id
        self.left_right = left_right
        self.is_visible = is_visible
        self.title = title
        self.description = description
        self.rank = rank

    def __repr__(self):
        return '<FeaturedStories %r>' % self.id

    @property
    def val_for_events(self):
        """
        JSON to store in Events 'new_value' field.
        """
        return {
            'id': self.id,
            'story_id': self.story_id,
            'left_right': self.left_right,
            'is_visible': self.is_visible,
            'title': self.title,
            'description': self.description,
            'rank': self.rank
        }


class Tags(db.Model):
    """
    Define the Stories class with the following columns:

    id - an integer containing the tag id
    name - a string containing the name of the tag
    """
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    @classmethod
    def populate(cls):
        """
        Automatically populates the tags table with tags from a predefined list
        """

        for item in tag.tags:
            tag_obj = Tags.query.filter_by(name=item).first()
            if tag_obj is None:
                tag_obj = Tags(name=item)
                db.session.add(tag_obj)
        db.session.commit()

    def __repr__(self):
        return '<Tags %r>' % self.name

    def __init__(self, name):
        self.name = name


class Comments(db.Model):
    """
    Define the Comments class with the following columns and relationships:

    id - and integer containing the comment id
    story_id - an integer containing the story id that a comment is related to
    name - a string containing the name of the commenter
    date_created - the date that the comment was created
    is_edited - a boolean that determines if the comment was edited or not.
    is_visible - a boolean that determines if the comment has been hidden from the public or not.
    """
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey("stories.id"))
    name = db.Column(db.String(60))
    content = db.Column(db.String(254), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    is_edited = db.Column(db.Boolean, nullable=False)
    is_visible = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return '<Comments %r>' % self.id

    def __init__(self,
                 story_id,
                 name,
                 content,
                 is_edited=False,
                 is_visible=True
                 ):
        self.story_id = story_id
        self.name = name
        self.content = content
        self.date_created = datetime.utcnow()
        self.is_edited = is_edited
        self.is_visible = is_visible


class Events(db.Model):
    """
    Define the Events class with the following columns and relationships:
    Events are used to create an audit trail of edits/deletes to stories and comments

    id - an integer that contains the event id
    story_id - an integer that contains the story id related to an event
    comment_id - an integer that contains the comment id related to an event
    module_id - an integer that contains the module id related to an event
    user_guid - a string that contains the user guid of the Admin/Mod that made the event
    type - an enum that contains the type of event that is made(edit, delete, etc.)
    timestamp - the date that the event was created
    previous_value - a JSON that contains the old content of a story or comment
    new_value - a JSON that contains the new content of a story or comment
    """
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey('stories.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'))
    user_guid = db.Column(db.String(64))
    type = db.Column(
        db.Enum(event_type.STORY_CREATED,
                event_type.USER_CREATED,
                event_type.EDIT_STORY,
                event_type.DELETE_STORY,
                event_type.EDIT_COMMENT,
                event_type.DELETE_COMMENT,
                event_type.ADD_FEATURED_STORY,
                event_type.EDIT_FEATURED_STORY,
                event_type.HIDE_FEATURED_STORY,
                event_type.EDIT_THEN_AND_NOW,
                event_type.STORY_FLAGGED,
                event_type.USER_EDITED,
                event_type.LOGIN_FAILED,
                event_type.LOGIN_SUCCESS,
                event_type.EMAIL_SENT,
                event_type.TAG_EDITED,
                event_type.TAG_DELETED,
                event_type.TAG_CREATED,
                event_type.NEW_SUBSCRIBER,
                event_type.UNSUBSCRIBED_EMAIL,
                event_type.UNSUBSCRIBED_PHONE,
                name='event_type'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    previous_value = db.Column(JSON)
    new_value = db.Column(JSON)

    def __repr__(self):
        return '<Events %r' % self.id

    def __init__(self,
                 _type,
                 story_id=None,
                 user_guid=None,
                 comment_id=None,
                 module_id=None,
                 previous_value=None,
                 new_value=None
                 ):
        self.story_id = story_id
        self.comment_id = comment_id
        self.module_id = module_id
        self.user_guid = user_guid
        self.type = _type
        self.timestamp = datetime.utcnow()
        self.previous_value = previous_value
        self.new_value = new_value


class Modules(db.Model):
    """
    Define the Modules class with the following columns and relationships:

    id - an integer that contains the module id
    story_id - an integer that contains the story id related to a module
    type - a string that contains the type of module being created
    title1 - a string that contains the main title of a module
    title2 - a string that contains the sub title of a module
    activist_first - a string that contains the first name of the activist in the module
    activist_last - a string that contains the last name of the activist in the module
    content - a string that contains the content of the module (either a short description or a quote)
    media_url - a string that contains the URL of the image or video associated with the module
    event_date - the date associated with the "Event" module
    activist_year - a string that contains the birth year of an activist (for then and now module)
    is_active - a boolean that to determine if this is the current module displayed on the site
    """
    __tablename__ = "modules"
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey('stories.id'))
    type = db.Column(
        db.Enum(module.FEATURED,
                module.THEN,
                module.NOW,
                module.EVENT,
                name='module_type'), nullable=False)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    activist_first = db.Column(db.String(128))
    activist_last = db.Column(db.String(128))
    content = db.Column(db.String(500))  # short description or quote
    media_url = db.Column(db.String(254))
    event_date = db.Column(db.DateTime)
    activist_year = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, nullable=False)

    @property
    def val_for_events(self):
        """
        JSON to store in Events 'new_value' field.
        """
        return {
            'id': self.id,
            'story_id': self.story_id,
            'type': self.type,
            'title': self.title,
            'subtitle': self.subtitle,
            'activist_first': self.activist_first,
            'activist_last': self.activist_last,
            'content': self.content,
            'media_url': self.media_url,
            'event_date': self.event_date,
            'activist_year': self.activist_year,
            'is_active': self.is_active
        }

    def __repr__(self):
        return '<Modules %r>' % self.id

    def __init__(self,
                 type,
                 story_id=None,
                 title=None,
                 subtitle=None,
                 activist_first=None,
                 activist_last=None,
                 content=None,
                 media_url=None,
                 event_date=None,
                 activist_year=None,
                 is_active=False
                 ):
        self.story_id = story_id
        self.type = type
        self.title = title
        self.subtitle = subtitle
        self.activist_first = activist_first
        self.activist_last = activist_last
        self.content = content
        self.media_url = media_url
        self.event_date = event_date
        self.activist_year = activist_year
        self.is_active = is_active


class Flags(db.Model):
    """
    Define the Flags class with the following columns and relationships:

    id - an integer that contains the flag id
    story_id - an integer that contains the story id of the story that is being flagged
    type - an enum that contains the type of flag that is being made (Inappropriate Content, Incorrect Information, Offensive Content, Other)
    reason - a string that contains a short description about why the user is flagging the story
    timestamp - the date of when the flag was submitted
    addressed - a boolean that determines whether or not an Admin/Mod has addressed the issues with the story
    """
    __tablename__ = "flags"
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey('stories.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    type = db.Column(
        db.Enum(flag.INAPPROPRIATE_CONTENT,
                flag.INCORRECT_INFORMATION,
                flag.OFFENSIVE_CONTENT,
                flag.OTHER,
                name='flag_type'))
    reason = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    addressed = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return '<Flags %r>' % self.id

    def __init__(self,
                 # id,
                 story_id,
                 # comment_id,
                 type,
                 reason,
                 addressed=False
                 ):
        # self.id = id
        self.story_id = story_id
        # self.comment_id = None # No comment functionality established yet
        self.type = type
        self.reason = reason
        self.timestamp = datetime.utcnow()
        self.addressed = addressed


class Feedback(db.Model):
    """
    Define the Feedback class with the following columns:

    id - an integer that contains the feedback id
    name - a string that contains the name of the user sending feedback
    email - a string that contains the email of the user sending feedback
    subject - a string that contains the subject of the feedback
    message -  a string that contains the message of the feedback
    timestamp - the date of when the feedback was submitted
    addressed - a boolean that determines whether or not an Admin/Mod has addressed the feedback or not
    """
    __tablename__ = "feedback"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    email = db.Column(db.String(254))
    subject = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    addressed = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return '<Feedback %r>' % self.title

    def __init__(self,
                 id,
                 name,
                 email,
                 subject,
                 message,
                 addressed=False
                 ):
        self.id = id
        self.name = name
        self.email = email
        self.subject = subject
        self.message = message
        self.timestamp = datetime.utcnow()
        self.addressed = addressed


class Subscribers(db.Model):
    """

    """
    __tablename__ = "subscribers"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    email = db.Column(db.String(254))
    phone = db.Column(db.String(25))

    def __init__(self,
                 first_name=None,
                 last_name=None,
                 email=None,
                 phone=None
                 ):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone


# flask requires the application to set up a callback function that loads a user, given the identifier
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)
