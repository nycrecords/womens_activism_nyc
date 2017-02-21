from flask import render_template
from app.catalog import catalog


@catalog.route('/', methods=['GET'])
def view():
    return render_template(
        'catalog/all.html',
    )
