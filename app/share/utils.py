from tempfile import NamedTemporaryFile
from flask import current_app
from werkzeug.utils import secure_filename
import os
# import base64


def move_upload(tmp_path):
    dst_dir = os.path.join(
        current_app.config['UPLOAD_DIRECTORY'])
    valid_name = os.path.basename(tmp_path).split('.', 1)[1]
    valid_path = os.path.join(dst_dir, valid_name)
    return valid_path


# def convert_and_save(image_pc, b64_string):
#     with open(image_pc.filename, "wb") as fh:
#         fh.write(base64.decodebytes(b64_string.encode()))

def handle_upload(file_field):
    path = upload(file_field.data)
    return path


def upload(image_pc):
    with NamedTemporaryFile(
        dir=current_app.config['UPLOAD_QUARANTINE_DIRECTORY'],
        suffix='.{}'.format(secure_filename(image_pc.filename)),
        delete=False
    ) as fp:
        image_pc.save(fp)
        return fp.name
