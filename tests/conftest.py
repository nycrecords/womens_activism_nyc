import pytest
from app import create_app, db
from app.models import Roles, Tags

@pytest.fixture
def app():
    app = create_app("testing")

    with app.app_context():
        Roles.metadata.create_all(db.engine)
        Tags.metadata.create_all(db.engine)
        Roles.populate()
        Tags.populate()

    yield app

    with app.app_context():
        db.session.remove()
        Roles.metadata.drop_all(db.engine)
        Tags.metadata.drop_all(db.engine)
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
