from flask import Flask

from config import DevelopmentConfig
from models import db as main_db
from models import login_manager
from importlib import import_module


def create_app():
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_object(DevelopmentConfig)
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
	main_db.init_app(app)
	login_manager.init_app(app)
	with app.app_context():
		from api_bp import api_bp
		from auth import auth_bp
		from logger import logger_bp
		from tracker import tracker_bp
		from users import user_bp
		from main import main_bp
		app.register_blueprint(api_bp, url_prefix='/api')
		app.register_blueprint(auth_bp)
		app.register_blueprint(tracker_bp, url_prefix='/tracker')
		app.register_blueprint(user_bp, url_prefix='/user')
		app.register_blueprint(main_bp, url_prefix='/main')
		app.register_blueprint(logger_bp, url_prefix='/logger')
	return app
