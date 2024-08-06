from app.share.views import upload_file
from app.share.forms import StoryForm
from app.models import Stories

from faker import Faker

fake = Faker(locale="en_US")

def test_new(app, client):
    with app.app_context():
        client.get('/share/').status_code == 200

        story = Stories(activist_first=fake.first_name(), activist_start=1924, activist_end=1984, activist_last=fake.last_name(), content=fake.text(200), tags="2",)
        form = StoryForm(formdata=None, obj=story, user_phone="", user_email=fake.email())

        response = client.post('/share', data=form.data, follow_redirects=True)
        assert len(response.history) == 2
        assert response.request.path == "/stories/1"


def test_upload_file(app, client):
    with app.app_context():
        # Test GET requests
        assert client.get('/share/upload-file').status_code == 400

        # Test empty POST requests
        with app.test_request_context("/share/upload-file", method='POST'):
            response = upload_file()
            assert response[1] == 400

        form_data = {
            'file': (open("resources/test-file.png", 'rb'), "test-file.png"),
            'final': 'true',
            'chunkindex': 0,
            'numchunks': 1,
            'chunkstart': 0,
            'filename': 'test-file.png'
        }

        # A necessary evil as the file had already been consumed, so it needs to be opened again each time
        def reset_file():
            form_data['file'] = (open("resources/test-file.png", 'rb'), "test-file.png")

        # Test file upload
        with app.test_request_context("/share/upload-file", method="POST", data=form_data):
            response = upload_file()
            assert response[1] == 201

        # Test incomplete upload
        reset_file()
        form_data['numchunks'] = 5
        with app.test_request_context("/share/upload-file", method="POST", data=form_data):
            response = upload_file()
            assert response[1] == 400

        # Test in progress upload
        reset_file()
        form_data['final'] = 'false'
        with app.test_request_context("/share/upload-file", method="POST", data=form_data):
            response = upload_file()
            assert response[1] == 204

