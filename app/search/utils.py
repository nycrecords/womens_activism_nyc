from flask import current_app

from app import es


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


def ccreate_docs():
    """
    Create elasticsearch request docs for every request stored in our db.
    """
    stories = Stories.query.all()

