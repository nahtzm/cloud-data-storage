from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from models import db
from models.file_model import File
from services.s3_service import upload_file_to_s3, generate_presigned_download, delete_s3_object

file_routes = Blueprint('file', __name__, url_prefix='/')


@file_routes.route('/upload', methods=['POST'])
@login_required
def upload_file():
    files = request.files.getlist('file')
    for file in files:
        s3_key = upload_file_to_s3(file, current_user.id, "cloud-data-storage-bucket")
        filename = secure_filename(file.filename)
        new_file = File(filename=filename, s3_key=s3_key, size=100, user_id=current_user.id)
        db.session.add(new_file)
    db.session.commit()
    flash(f"{len(files)} file(s) uploaded successfully", "success")
    return redirect(url_for('main.dashboard'))


@file_routes.route('/download/<int:file_id>')
@login_required
def download_file(file_id):
    file = File.query.filter_by(id=file_id, user_id=current_user.id).first()
    if not file:
        flash("File not found", "error")
        return redirect(url_for('main.dashboard'))
    url = generate_presigned_download(file, "cloud-data-storage-bucket", file.s3_key)
    return redirect(url)


@file_routes.route('/delete/<int:file_id>', methods=['POST'])
@login_required
def delete_file(file_id):
    file = File.query.filter_by(id=file_id, user_id=current_user.id).first()
    if not file:
        flash("File not found", "error")
        return redirect(url_for('main_route.dashboard'))
    delete_s3_object(
        "cloud-data-storage-bucket",

        file.s3_key
    )

    db.session.delete(file)
    db.session.commit()

    flash('File deleted', category='success')
    return redirect(url_for('main.dashboard'))
