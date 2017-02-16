from flask import current_app
from elasticsearch.helpers import bulk

from app import es
from app.models import Stories
from app.search.constants import MOCK_EMPTY_ELASTICSEARCH_RESULT


def create_index():
    """
    Create elasticsearch index with mappings for stories docs.
    """
    es.indices.create(
        index=current_app.config["ELASTICSEARCH_INDEX"],
        body={
            "mappings": {
                "story": {
                    "properties": {
                        "key": {
                            "type": "keyword"
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
            'tag': s.tags
        })

    num_success, _ = bulk(
        es,
        operations,
        index=current_app.config["ELASTICSEARCH_INDEX"],
        doc_type='story',
        chunk_size=100,
        raise_on_error=True
    )
    print("Successfully created %s docs." % num_success)


def update_docs():
    stories = Stories.query.all()
    for s in stories:
        s.es_update()


def search_stories(query,
                   activist_first,
                   activist_last,
                   content,
                   tag,
                   by_phrase=False,
                   highlight=False):
    """
    The arguments of this function match the request parameters
    of the '/search/stories' endpoints.

    :param query: string to query for
    :param activist_first: search by activist's first name?
    :param activist_last: search by activist's last name?
    :param content: search by story content?
    :param tag: search by tag
    :param by_phrase: use phrase matching instead of full-text?
    :param highlight: return highlights?
        if True, will come at a slgiht performance cost (in order to
        restrict highlights to public fields, iterating over elasticsearch
        query results is required)
    :return: elasticsearch json response with result information
    """
    # clean query trailing/leading whitespace
    if query is not None:
        query = query.strip()

    # return no results if there is nothing to query by
    if query and not any((activist_first, activist_last, content, tag)):
        return MOCK_EMPTY_ELASTICSEARCH_RESULT

    # set matching type (full-text or phrase matching)
    match_type = 'match_phrase' if by_phrase else 'match'

    # generate query dsl body
    query_fields = {
        'activist_first': activist_first,
        'activist_last': activist_last,
        'content': content,
        'tag': tag
    }
    dsl_gen = StoriesDSLGenerator(query, query_fields, match_type)


class StoriesDSLGenerator(object):
    """
    Class for generating dicts representing query dsl bodies for searching story docs.
    """
    def __init__(self, query, query_fields, match_type):
        self.__query = query
        self.__query_fields = query_fields
        self.__match_type = match_type

