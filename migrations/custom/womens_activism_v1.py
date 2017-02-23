import psycopg2.extras
from uuid import uuid4

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


def transfer_tags_in_v1():
    # Add tags column to stories table
    CUR_V1.execute("ALTER TABLE stories ADD COLUMN tags VARCHAR(50)[];")
    CUR_V1.execute("SELECT * FROM story_tags")
    story_tags = CUR_V1.fetchall()
    for story_tag in story_tags:
        tag_name = TAG_ID_TO_NAME[story_tag.tag_id]
        if story_tag.story_id not in TAG_TO_STORY_ID:
            TAG_TO_STORY_ID[story_tag.story_id] = [tag_name]
        else:
            TAG_TO_STORY_ID[story_tag.story_id].append(tag_name)
    for key in TAG_TO_STORY_ID.keys():
        query = ("UPDATE stories SET tags=%s WHERE id=%s")
        CUR_V1.execute(query, (
            TAG_TO_STORY_ID[key],
            key
        ))
        CONN_V1.commit()


def transfer_stories():
    # Add tags column to stories table
    CUR_V1.execute("ALTER TABLE stories ADD COLUMN tags VARCHAR(50)[];")
    CUR_V1.execute("SELECT * FROM stories")


if __name__ == "__main__":
    transfer_tags_in_v1()