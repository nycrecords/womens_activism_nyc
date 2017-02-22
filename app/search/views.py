from flask import (
    request,
    render_template,
    jsonify
)

from app.search import search
from app.search.constants import DEFAULT_HITS_SIZE, DEFAULT_START_NUMBER
from app.search.utils import search_stories


@search.route("/stories", methods=['GET'])
def stories():
    """
    For story parameters, see app.search.utils.search_stories

    Users can search by:
    - Activist First Name
    - Activist Last Name
    - Content

    Users can filter by:
    - Tags
    """
    try:
        size = int(request.args.get('size', DEFAULT_HITS_SIZE))
    except ValueError:
        size = DEFAULT_HITS_SIZE

    try:
        start = int(request.args.get('start'), DEFAULT_START_NUMBER)
    except ValueError:
        start = DEFAULT_START_NUMBER

    query = request.args.get('query')
    search_tags = []
    results = search_stories(
        query,
        search_tags,
        size,
        start
    )

    # format results
    total = results["hits"]["total"]
    formatted_results = None
    if total != 0:
        formatted_results = render_template("catalog/result.html",
                                            stories=[r['_source'] for r in results['hits']['hits']])
    return jsonify({
        "count": len(results["hits"]["hits"]),
        "total": total,
        "results": formatted_results
    }), 200
