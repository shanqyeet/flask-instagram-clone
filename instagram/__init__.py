import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from werkzeug.utils import secure_filename

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpeg', 'jpg', 'gif'])

csrf = CSRFProtect()
app = Flask(__name__, template_folder='templates')
csrf.init_app(app)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.urandom(24).hex()
login = LoginManager(app)

db = SQLAlchemy(app)
Migrate(app, db)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

from instagram.users.views import user
app.register_blueprint(user)
import instagram.views
import instagram.users.views

print(app.url_map)
if __name__ == '__main__':
    app.run()
