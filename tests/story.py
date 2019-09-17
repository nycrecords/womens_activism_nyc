import random
from itertools import product

from app import db
from app.constants import tag
from app.models import Stories


def create_stories_search_set():
    for activist_first, activist_last, content in product(
        ("foo", "bar", "qux"), repeat=3
    ):
        story = Stories(
            activist_first=activist_first,
            activist_last=activist_last,
            activist_start=1917,
            activist_end=1920,
            content=content,
            tags=[random.choice(tag.tags)],
        )
        db.session.add(story)
        db.session.commit()
