from tempfile import NamedTemporaryFile
from flask import current_app
from werkzeug.utils import secure_filename
#from flask import request


def handle_upload(file_field):
    path = upload(file_field.data)
    return path


# files = request.files
# file_ = files[next(files.keys())]
# filename = secure_filename(file_.filename)


def upload(image_pc):
    with NamedTemporaryFile(
        dir=current_app.config['UPLOAD_QUARANTINE_DIRECTORY'],
        suffix='.{}'.format(secure_filename(image_pc.filename)),
        delete=False
    ) as fp:
        image_pc.save(fp)
        return fp.name
