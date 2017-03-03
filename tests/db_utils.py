import random
from unittest.mock import patch

from tests.lib.base import BaseTestCase
from tests.lib.tools import create_user

from app.constants import tag
from app.lib.db_utils import create_object
from app.models import Stories, Users


class CreateObjectTests(BaseTestCase):
    """
    Class for testing create object function.
    """
    def test_object_created(self):
        self.assertFalse(Users.query.first())
        create_user()
        self.assertTrue(Users.query.first())

    def test_es_doc_not_created(self):
        try:
            create_user()
        except AttributeError:
            self.fail('es_created method called when it should not have been.')

    @patch('app.models.Stories.es_create')
    def test_story_es_doc_not_created(self, es_create_patch):
        create_object(Stories(
            activist_first='John',
            activist_last='Doe',
            content='This is the content of my story.',
            tags=[random.choice(tag.tags)],
            activist_start=random.randint(0, 2017),
            activist_end=random.randint(0, 2017),
            activist_url='https://womensactivism.nyc'
        ))
        self.assertFalse(es_create_patch.called)
