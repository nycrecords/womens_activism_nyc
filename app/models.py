from app import db
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON
from app.constants import permission, role_name, tag_list, user_type_auth


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


class User(UserMixin, db.Model):
    """
    Define the User class with the following columns and relationships:

    guid - an integer that contains the guid of a user, part of a compositie primary key
    auth_user_type - an integer that contains that authentification type of a user, part of a composite primary key
    is_mod - a boolean that determines if a user is a moderator or not
    is_admin - a boolean that determines if a user is an admin or not
    first_name - a string that contains the first name of the user
    middle_initial - a string the contains the middle initial of the user
    last_name - a string that contains the last name of the user
    email - a string that contains the email of the user
    """

    __tablename__ = "users"
    guid = guid = db.Column(db.String(64), primary_key=True)
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
                name='auth_user_type'))
    is_mod = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    first_name = db.Column(db.String(32))
    middle_initial = db.Column(db.String(1))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(254))
    email_validated = db.Column(db.Boolean())
    terms_of_use_accepted = db.Column(db.Boolean)

    def __repr__(self):
        return '<User %r>' % self.guid


class Posters(db.Model):
    __tablename__ = "posters"
    id = db.Column(db.Integer, primary_key=True)
    poster_first = db.Column(db.String(30))
    poster_last = db.Column(db.String(30))
    email = db.Column(db.String(254))


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
    is_edited - a boolean that determines if the story was edited. True = the story was edited, False = the story was not edited
    is_visible - a boolean that determines if the story has been hidden from the public. True = the story has been hidden, False = the story has not been hidden
    """

    __tablename__ = "stories"
    id = db.Column(db.Integer, primary_key=True)
    activist_first = db.Column(db.String(30))
    activist_last = db.Column(db.String(30))
    activist_start = db.Column(db.Integer)
    activist_end = db.Column(db.Integer)
    content = db.Column(db.Text)
    activist_url = db.Column(db.Text)
    image_url = db.Column(db.Text)
    video_url = db.Column(db.Text)
    poster_id = db.Column(db.Integer, db.ForeignKey("posters.id"))
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    is_edited = db.Column(db.Boolean, default=False)
    is_visible = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return '<Stories %r>' % self.id

    def __init__(
            self,
            activist_first,
            activist_last,
            content,
            activist_url,
            image_url,
            video_url,
            poster_id,
            date_created=datetime.utcnow(),
            is_edited=False,
            is_visible=True
    ):
        self.activist_first = activist_first
        self.activist_last = activist_last
        self.content = content
        self.activist_url = activist_url
        self.image_url = image_url
        self.video_url = video_url
        self.poster_id = poster_id
        self.date_created = date_created
        self.is_edited = is_edited
        self.is_visible = is_visible


class Tags(db.Model):
    """
    Define the Stories class with the following columns:

    id - an integer containing the tag id
    name - a string containing the name of the tag
    """

    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    @classmethod
    def populate(cls):
        """
        Automatically populates the tags table with tags from a predefined list
        """

        for tag in tag_list.tags:
            tag_obj = Tags.query.filter_by(name=tag).first()
            if tag_obj is None:
                tag_obj = Tags(name=tag)
                db.session.add(tag_obj)
        db.session.commit()

    def __repr__(self):
        return '<Tags %r>' % self.name

    def __init__(self, name):
        self.name = name


class StoryTag(db.Model):
    """
    Define the StoryTag class with the following columns:
    a StoryTag is a relationship between which tags are associated a story
    one story can have many tags but each tag is stored in its own row
    story_id and tag_id are combined to make a composite primary key


    story_id - an integer containing the story id
    tag_id - an integer containing the tag id

    """

    __tablename__ = "story_tags"
    story_id = db.Column(db.Integer, db.ForeignKey("stories.id"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)

    def __repr__(self):
        return '<StoryTag %r>' % self.story_id

    def __init__(self,
                 story_id,
                 tag_id
                 ):
        self.story_id = story_id
        self.tag_id = tag_id


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
    content = db.Column(db.String(140))
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    is_edited = db.Column(db.Boolean)
    is_visible = db.Column(db.Boolean)

    def __repr__(self):
        return '<Comments %r>' % self.id

    def __init__(self,
                 story_id,
                 name,
                 content,
                 date_created=datetime.utcnow(),
                 is_edited=False,
                 is_visible=True
                 ):
        self.story_id = story_id
        self.name = name
        self.content = content
        self.date_created = date_created
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
    user_guid = db.Column(db.String(64), db.ForeignKey('users.guid'))
    type = db.Column(
        db.Enum('Edit Story',
                'Delete Story',
                'Edit Comment',
                'Delete Comment',
                'Edit Featured Story',
                'Edit Then and Now',
                'Edit Event',
                name='type'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    previous_value = db.Column(JSON)
    new_value = db.Column(JSON)

    def __repr__(self):
        return '<Events %r' % self.id

    def __init__(self,
                 id,
                 story_id,
                 comment_id,
                 module_id,
                 user_guid,
                 type,
                 timestamp=datetime.utcnow(),
                 previous_value=None,
                 new_value=None
                 ):
        self.id = id
        self.story_id = story_id
        self.comment_id = comment_id
        self.module_id = module_id
        self.user_guid = user_guid,
        self.type = type,
        self.timestamp = timestamp,
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
    """

    __tablename__ = "modules"
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey('stories.id'))
    type = db.Column(
        db.Enum('Featured',
                'Then',
                'Now',
                'Event',
    name = 'type'))
    title1 = db.Column(db.String(50))
    title2 = db.Column(db.String(50))
    activist_first = db.Column(db.String(30))
    activist_last = db.Column(db.String(30))
    content = db.Column(db.String(500))  # short description or quote
    media_url = db.Column(db.Text)
    event_date = db.Column(db.DateTime)
    activist_year = db.Column(db.String(4))

    def __repr__(self):
        return '<Modules %r' % self.id

    def __init__(self,
                 id,
                 story_id,
                 type,
                 title1,
                 title2,
                 activist_first,
                 activist_last,
                 content,
                 media_url,
                 event_date,
                 activist_year
                 ):
        self.id = id
        self.story_id = story_id
        self.type = type
        self.title1 = title1
        self.title2 = title2
        self.activist_first = activist_first
        self.activist_last = activist_last
        self.content = content
        self.media_url = media_url
        self.event_date = event_date
        self.activist_year = activist_year


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
        db.Enum('Inappropriate Content',
                'Incorrect Information',
                'Offensive Content',
                'Other',
    name = 'type'))
    reason = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    addressed = db.Column(db.Boolean)

    def __repr__(self):
        return '<Flags %r>' % self.id

    def __init__(self,
                 id,
                 story_id,
                 comment_id,
                 type,
                 reason,
                 timestamp=datetime.utcnow(),
                 addressed=False
                 ):
        self.id = id
        self.story_id = story_id
        self.comment_id = comment_id
        self.type = type
        self.reason = reason
        self.timestamp = timestamp
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
    subject = db.Column(db.String(50))
    message = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    addressed = db.Column(db.Boolean)

    def __repr__(self):
        return '<Feedback %r>' % self.title

    def __init__(self,
                 id,
                 name,
                 email,
                 subject,
                 message,
                 timestamp=datetime.utcnow(),
                 addressed=False
                 ):
        self.id = id
        self.name = name
        self.email = email
        self.subject = subject
        self.message = message
        self.timestamp = timestamp
        self.addressed = addressed