from flask import Blueprint, render_template
from flask_login import login_required, current_user

from models.file_model import File

main_route = Blueprint('main', __name__)

@main_route.route('/')
def home():
    return render_template("home.html")

@main_route.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    files = File.query.filter_by(user_id=current_user.id).order_by(File.id.desc()).all()

    return render_template("dashboard.html", files=files)

