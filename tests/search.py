from flask import current_app, render_template, json

from tests.lib.base import BaseTestCase
from tests.lib.constants import ELASTICSEARCH_SUCCESS_DOCS
from tests.lib.tools import create_sample_stories

from app import db, es
from app.models import Stories
from app.search.utils import (
    create_index,
    create_docs,
    search_stories,
)


class SearchViewsTests(BaseTestCase):
    def setUp(self):
        super(SearchViewsTests, self).setUp()
        create_sample_stories()
        create_index()
        create_docs()

    def tearDown(self):
        es.indices.delete(current_app.config['ELASTICSEARCH_INDEX'],
                          ignore=[400, 404])
        super(SearchViewsTests, self).tearDown()

    def test_stories_post_query_all(self):
        response = self.client.get(
            'search/stories?query=&tags=&size=&start='
        )

        results = search_stories(query='',
                                 search_tags=[],
                                 size=40,
                                 start=0)
        formatted_results = render_template('stories/result.html',
                                            stories=results['hits']['hits'])

        self.assertEqual(
            json.loads(response.data.decode()),
            {
                'count': ELASTICSEARCH_SUCCESS_DOCS,
                'total': ELASTICSEARCH_SUCCESS_DOCS,
                'results': formatted_results
            }
        )

    def test_stories_post_query_one(self):
        response = self.client.get(
            'search/stories?query=Mary&tags=&size=&start='
        )

        results = search_stories(query='Mary',
                                 search_tags=[],
                                 size=40,
                                 start=0)
        formatted_results = render_template('stories/result.html',
                                            stories=results['hits']['hits'])

        self.assertEqual(
            json.loads(response.data.decode()),
            {
                'count': 1,
                'total': 1,
                'results': formatted_results
            }
        )


class SearchUtilsTests(BaseTestCase):
    def setUp(self):
        super(SearchUtilsTests, self).setUp()
        self.es_index = current_app.config['ELASTICSEARCH_INDEX']
        create_sample_stories()

    def tearDown(self):
        es.indices.delete(self.es_index,
                          ignore=[400, 404])
        db.session.query(Stories).delete()
        super(SearchUtilsTests, self).tearDown()

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
