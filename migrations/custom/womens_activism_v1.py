import psycopg2.extras
import uuid

from app.lib.date_utils import local_to_utc
from app.constants import user_type_auth

TAG_ID_TO_NAME = {
    1: "Abolition",
    2: "Arts and Entertainment",
    3: "Business and Entrepreneurship",
    4: "Civil and Human Rights",
    5: "Education",
    6: "Environment",
    7: "Government and Politics",
    8: "Health",
    9: "LGBTQ",
    10: "Law",
    11: "Literature and Journalism",
    12: "Military",
    13: "Religion",
    14: "Science, Technology, Engineering and Math (STEM)",
    15: "Sports",
    16: "Suffrage",
    17: "Other"
}

CONN_V1 = psycopg2.connect(database='womens_activism_v1',
                           user='postgres',
                           host='localhost',
                           port='5432',
                           sslmode=None)
CONN_V2 = psycopg2.connect(database='womens_activism_dev',
                           user='postgres',
                           host='localhost',
                           port='5432',
                           sslmode=None)
CUR_V1 = CONN_V1.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
CUR_V2 = CONN_V2.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)

TAG_TO_STORY_ID = {}

TZ_NY = 'US/Eastern'
TODAY_INTEGER_VALUE = 9999


def transfer_tags_in_v1():
    """
    Transfer tags in v1 from story_tags table to stories table
    """
    # Add tags column to stories table
    # CUR_V1.execute("ALTER TABLE stories ADD COLUMN tags VARCHAR(50)[];")
    CUR_V1.execute("SELECT * FROM story_tags")
    story_tags = CUR_V1.fetchall()

    for story_tag in story_tags:
        # Get tag name from dictionary mapping
        tag_name = TAG_ID_TO_NAME[story_tag.tag_id]

        # Append to dictionary with story_id as key and list of tag names as value
        if story_tag.story_id not in TAG_TO_STORY_ID:
            TAG_TO_STORY_ID[story_tag.story_id] = [tag_name]
        else:
            TAG_TO_STORY_ID[story_tag.story_id].append(tag_name)

    # Transfer tags from dictionary to stories table in v1
    for key in TAG_TO_STORY_ID.keys():
        query = ("UPDATE stories SET tags=%s WHERE id=%s")

        CUR_V1.execute(query, (
            TAG_TO_STORY_ID[key],
            key
        ))

        CONN_V1.commit()


def transfer_stories(user_ids_to_guids):
    """
    Transfer stories from v1 to v2.
    Convert string year to integer if year is not empty.
    Convert local EST datetime creation_time to utc.

    :param user_ids_to_guids: dictionary with key of user.id and value of guid.
    """
    CUR_V1.execute("SELECT * FROM stories")

    for story in CUR_V1.fetchall():
        query = ("INSERT INTO stories("
                 "id,"
                 "activist_first,"
                 "activist_last,"
                 "activist_start,"
                 "activist_end,"
                 "content,"
                 "activist_url,"
                 "image_url,"
                 "video_url,"
                 "user_guid,"
                 "date_created,"
                 "is_edited,"
                 "is_visible,"
                 "tags)"
                 "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

        if story.activist_end:
            end_year = TODAY_INTEGER_VALUE if story.activist_end == 'Today' else int(story.activist_end)
        else:
            end_year = None

        if story.activist_start and story.activist_start != '?':
            start_year = int(story.activist_start)
        else:
            start_year = None

        CUR_V2.execute(query, (
            story.id,
            story.activist_first,
            story.activist_last,
            start_year,
            end_year,
            story.content,
            story.activist_url,
            story.image_link,
            story.video_link,
            user_ids_to_guids[story.poster_id] if story.poster_id in user_ids_to_guids else None,
            local_to_utc(story.creation_time, TZ_NY),
            story.is_edited,
            story.is_visible,
            story.tags
        ))

        CONN_V2.commit()


def transfer_users(user_ids_to_guids):
    """
    Transfer users from v1 to v2.
    All users transferred are anonymous.
    Create guids for users from v1.

    :param user_ids_to_guids: empty dictionary that will be populated
    """
    CUR_V1.execute("SELECT * FROM users")

    auth_user_type = user_type_auth.ANONYMOUS_USER

    for user in CUR_V1.fetchall():
        guid = str(uuid.uuid4())
        user_ids_to_guids[user.id] = guid

        query = ("INSERT INTO users("
                 "guid,"
                 "auth_user_type,"
                 "is_mod,"
                 "is_admin,"
                 "first_name,"
                 "middle_initial,"
                 "last_name,"
                 "email,"
                 "email_validated,"
                 "terms_of_use_accepted)"
                 "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

        CUR_V2.execute(query, (
            guid,
            auth_user_type,
            False,
            False,
            user.first_name,
            None,
            user.last_name,
            user.email,
            False,
            False
        ))

        CONN_V2.commit()


def transfer_all():
    """
    Migrate all data from v1 to v2 db (call all transfer functions).
    """
    transfer_tags_in_v1()
    user_ids_to_guids = {}
    transfer_users(user_ids_to_guids)
    transfer_stories(user_ids_to_guids)

if __name__ == "__main__":
    transfer_all()
