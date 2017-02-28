from elasticsearch.helpers import bulk
from flask import current_app

from app import es
from app.constants import tag
from app.constants.search import ALL_RESULTS_CHUNKSIZE
from app.models import Stories


def recreate():
    """Delete current index and create new index and docs"""
    es.indices.delete(current_app.config["ELASTICSEARCH_INDEX"],
                      ignore=[400, 404])
    create_index()
    create_docs()


def create_index():
    """
    Create elasticsearch index with mappings for stories docs.
    """
    es.indices.create(
        index=current_app.config["ELASTICSEARCH_INDEX"],
        body={
            "settings": {
                "analysis": {
                    "tokenizer": {
                        "ngram_tokenizer": {
                            "type": "ngram",
                            "min_gram": 1,
                            "max_gram": 6
                        }
                    },
                    "analyzer": {
                        "ngram_tokenizer_analyzer": {
                            "type": "custom",
                            "tokenizer": "ngram_tokenizer",
                            "filter": [
                                "lowercase"
                            ]
                        }
                    }
                }
            },
            "mappings": {
                "story": {
                    "properties": {
                        "activist_first": {
                            "type": "text",
                            "analyzer": "ngram_tokenizer_analyzer",
                            "fields": {
                                "exact": {
                                    "type": "text",
                                    "analyzer": "standard",
                                },
                            },
                        },
                        "activist_last": {
                            "type": "text",
                            "analyzer": "ngram_tokenizer_analyzer",
                            "fields": {
                                "exact": {
                                    "type": "text",
                                    "analyzer": "standard",
                                },
                            },
                        },
                        "content": {
                            "type": "text",
                        },
                        "tag": {
                            "type": "keyword"
                        }
                    }
                }
            }
        }
    )


def create_docs():
    """
    Create elasticsearch request docs for every request stored in our db.
    """
    stories = Stories.query.all()

    operations = []
    for s in stories:
        operations.append({
            '_op_type': 'create',
            '_id': s.id,
            'activist_first': s.activist_first,
            'activist_last': s.activist_last,
            'content': s.content,
            'image_url': s.image_url,
            'tag': s.tags
        })

    num_success, _ = bulk(
        es,
        operations,
        index=current_app.config["ELASTICSEARCH_INDEX"],
        doc_type='story',
        chunk_size=ALL_RESULTS_CHUNKSIZE,
        raise_on_error=True
    )
    print("Successfully created %s docs." % num_success)


def update_docs():
    """Update elasticsearch index"""
    stories = Stories.query.all()
    for s in stories:
        s.es_update()


def search_stories(query,
                   # activist_first,
                   # activist_last,
                   # content,
                   search_tags,
                   size,
                   start):
    """
    The arguments of this function match the request parameters
    of the '/search/stories' endpoints.

    :param query: string to query for
    NOTE: activist_first, activist_last, and content are currently
    being searched by default and thus are not inputs
    :param activist_first: search by activist's first name?
    :param activist_last: search by activist's last name?
    :param content: search by story content?
    :param search_tags: search by tag
    :param size: number of stories
    :param start: starting index of story result set
    :param by_phrase: use phrase matching instead of full-text?
    :return: elasticsearch json response with result information
    """
    # clean query trailing/leading whitespace
    if query is not None:
        query = query.strip()

    tags = search_tags if search_tags else tag.tags

    # set matching type (full-text or phrase matching)
    match_type = 'multi_match'

    # generate query dsl body
    query_fields = {
        'activist_first': True,
        'activist_first.exact': True,
        'activist_last': True,
        'activist_last.exact': True,
        'content': True,
    }
    dsl_gen = StoriesDSLGenerator(query, query_fields, tags, match_type)
    dsl = dsl_gen.search() if query else dsl_gen.queryless()

    # search/run query
    results = es.search(
        index=current_app.config["ELASTICSEARCH_INDEX"],
        doc_type='story',
        body=dsl,
        _source=['activist_first',
                 'activist_last',
                 'content',
                 'image_url',
                 'tag'],
        size=size,
        from_=start,
    )

    return results


class StoriesDSLGenerator(object):
    """
    Class for generating dicts representing query dsl bodies for searching story docs.
    """
    def __init__(self, query, query_fields, tags, match_type):
        """
        Constructor for class StoriesDSLGenerator

        :param query: string to query for
        :param query_fields: fields to query by
        :param tags: tags to query by
        :param match_type: type of query
        """
        self.__query = query
        self.__query_fields = query_fields
        self.__match_type = match_type

        self.__default_filters = [{'terms': {'tag': tags}}]
        self.__filters = []
        self.__conditions = []

    def search(self):
        """
        Generate dictionary of generic search query
        :return: dictionary with prepended method __should
        """
        self.__filters = [
            {self.__match_type: {
                "query": self.__query,
                "fields": [name for name in self.__query_fields.keys()],
                "type": "most_fields",
                "minimum_should_match": "75%"
            }}
        ]
        self.__conditions.append(self.__must)
        return self.__should

    def queryless(self):
        """
        Generate dictionary of search query that queries all
        :return: dictionary with prepended method __must
        """
        self.__filters = [
            {'match_all': {}}
        ]
        return self.__must_query

    @property
    def __must_query(self):
        """
        :return: dictionary with key of 'query' and value of __must method
        """
        return {
            'query': self.__must
        }

    @property
    def __must(self):
        """
        :return: dictionary with key of 'bool' and value of __get_filters method
        """
        return {
            'bool': {
                'must': self.__get_filters()
            }
        }

    @property
    def __should(self):
        """
        dictionary header representing dsl query bodies
        :return: nested dictionary
        """
        return {
            'query': {
                'bool': {
                    'should': self.__conditions
                }
            }
        }

    def __get_filters(self):
        """
        :return: combine dicts from __filter and __default_filters methods
        """
        return self.__filters + self.__default_filters
