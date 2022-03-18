from flask import Flask
from .api_bp import api_bp
from .auth import auth_bp
from .logger import logger_bp
from .tracker import tracker_bp
from .users import user_bp
from models import db as main_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
main_db.init_app(app)
app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(tracker_bp, url_prefix='/tracker')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(logger_bp, url_prefix='/logger')


if __name__ == '__main__':
    app.run(debug=True)
