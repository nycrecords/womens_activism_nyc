import random

from flask import current_app

from tests.lib.base import BaseTestCase
from tests.lib.constants import ELASTICSEARCH_SUCCESS_DOCS

from app import db, es
from app.constants import tag
from app.models import Stories
from app.search.utils import (
    create_index,
    create_docs,
    search_stories,
)


class SearchUtilsTests(BaseTestCase):
    def setUp(self):
        super(SearchUtilsTests, self).setUp()
        self.es_index = current_app.config['ELASTICSEARCH_INDEX']
        self.create_sample_stories()

    def tearDown(self):
        es.indices.delete(self.es_index,
                          ignore=[400, 404])
        db.session.query(Stories).delete()
        super(SearchUtilsTests, self).tearDown()

    def create_sample_stories(self):
        objects = [
            Stories(activist_first='Jane',
                    activist_last='Doe',
                    content='The story of Jane.',
                    tags=[random.choice(tag.tags)]),
            Stories(activist_first='Mary',
                    activist_last='Smith',
                    content='The story of Mary.',
                    tags=[random.choice(tag.tags)]),
        ]
        db.session.add_all(objects)
        db.session.commit()

    def test_index_created(self):
        self.assertFalse(es.indices.exists(index=self.es_index))
        create_index()
        self.assertTrue(es.indices.exists(index=self.es_index))

    def test_docs_created(self):
        create_index()
        self.assertEqual(ELASTICSEARCH_SUCCESS_DOCS, create_docs())

    def test_search_stories_match_all(self):
        create_index()
        create_docs()
        results = search_stories(query='',
                                 search_tags=[],
                                 size=10,
                                 start=0)['hits']['total']
        self.assertEqual(ELASTICSEARCH_SUCCESS_DOCS, results)
