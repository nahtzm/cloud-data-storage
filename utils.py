import os
from flask import current_app
from flask_login import current_user
from models.file_model import File


def get_file_filepath_by_id(file_id):
    file = File.query.filter_by(
        id=file_id,
        user_id=current_user.id
    ).first()

    if not file:
        return None, None

    user_folder = os.path.join(
        current_app.config['UPLOAD_FOLDER'],
        f"user_{current_user.id}"
    )
    file_path = os.path.join(user_folder, file.filename)

    return file, file_path
