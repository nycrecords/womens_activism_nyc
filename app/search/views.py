from flask import (
    request,
    render_template,
    jsonify
)

from app.search import search
from app.search.constants import DEFAULT_HITS_SIZE
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
        start = int(request.args.get('start'), 0)
    except ValueError:
        start = 0

    query = request.args.get('query')
    results = search_stories(
        query,
        size,
        start
    )

    # format results
    total = results["hits"]["total"]
    formatted_results = None
    if total != 0:
        formatted_results = render_template("catalog/result_row.html",
                                            stories=results["hits"]["hits"])
    return jsonify({
        "count": len(results["hits"]["hits"]),
        "total": total,
        "results": formatted_results
    }), 200
