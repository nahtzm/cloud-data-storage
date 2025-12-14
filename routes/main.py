from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import func

from models import db
from models.file_model import File
from models.plan_model import PLANS

main_route = Blueprint('main', __name__)

@main_route.route('/')
def home():
    return render_template("home.html")

@main_route.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    used_storage = db.session.query(
        func.coalesce(func.sum(File.size), 0)
    ).filter(
        File.user_id == current_user.id
    ).scalar()

    plan = PLANS[current_user.plan]
    max_storage = plan.storage_limit
    percent = min(int((used_storage / max_storage) * 100), 100)

    files = File.query.filter_by(user_id=current_user.id).order_by(File.id.desc()).all()

    return render_template("dashboard.html",
                           files=files,
                           used_storage=used_storage,
                           percent=percent,
                           plan=plan,
                           max_storage=max_storage )

@main_route.route('/upgrade/<plan>')
@login_required
def upgrade(plan):
    current_user.plan = plan
    db.session.commit()
    #
    flash("Plan upgraded successfully!", "success")
    return redirect(url_for("main.dashboard"))

@main_route.route('/billing', methods=['GET', 'POST'])
@login_required
def billing():

    return render_template("billing.html", plans= PLANS, current_plan=current_user.plan)
