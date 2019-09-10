from tempfile import NamedTemporaryFile
from flask import current_app
from werkzeug.utils import secure_filename
import os
from app import s3
import subprocess


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
        data = open(fp.name, 'rb')
        fp.name = fp.name.split('.', 1)[1]
        s3.Bucket('nycrecords-wom-uploads-dev').put_object(Key=fp.name, Body=data, ACL='public-read', ContentType='image/jpeg')
        subprocess.call([
            "rm",
            "-rf",
            fp.name,
        ])
        return fp.name
