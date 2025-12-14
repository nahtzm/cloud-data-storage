from flask import Flask
from flask_login import LoginManager

from config import config
from routes.auth import auth
from routes.file import file_routes
from routes.main import main_route
from models import db
from models.user_model import User

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
app.register_blueprint(auth, url_prefix='/')
app.register_blueprint(file_routes, url_prefix='/')
app.register_blueprint(main_route, url_prefix='/')

login = LoginManager()
login.login_view = 'auth.login'
login.init_app(app)


@login.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


if __name__ == '__main__':
    app.run(debug=True)
