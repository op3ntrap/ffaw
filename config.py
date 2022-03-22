import os

basedir = os.path.abspath(os.path.dirname(__name__))


# MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.googlemail.com")
# MAIL_PORT = int(os.environ.get("MAIL_PORT", "587"))
# MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "true").lower() in ["true", "on", "1"]
# MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
# MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
# QS_MAIL_SUBJECT_PREFIX = "[QS]"
# QS_SENDER = "QS Admin <21f1000021@student.onlinedegree.iitm.ac.in>"
# QS_admin = os.environ.get("QS_ADMIN")
class Config:
	SECRET_KEY = 'uO-i2UdP8T_K0AvH974Z3eUREgBd1Bso3doBZfJpLwX_l2qyzY6yG_q0LCsJL25lkj0yqeVDpBM06G0WHap85A'
	JSON_SORT_KEYS = False
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	JSONIFY_PRETTYPRINT_REGULAR = True
	TEMPLATES_AUTO_RELOAD = True
	ENV = 'development'
	PERMANENT_SESSION_LIFETIME = 2678400

	@staticmethod
	def init_app(app):
		pass


class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = "sqlite:///data.sqlite3"


class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = "sqlite:///data.sqlite3"


class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = "sqlite:///data.sqlite3"


config = {
	"development": DevelopmentConfig,
	"testing"    : TestingConfig,
	"production" : ProductionConfig,
	"default"    : DevelopmentConfig,
}
