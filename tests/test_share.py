from app.share.views import upload_file


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

