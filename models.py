import datetime
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from auth.tools import hash_pass

# from . import login_manager as authentication_manager

db = SQLAlchemy()
login_manager = LoginManager()

# login_manager = LoginManager()

public_user_trackers = db.Table('public_user_trackers',
                                db.Column('user_tracker_id', db.Integer, primary_key=True, autoincrement=True),
                                db.Column('user_id', db.Integer, db.ForeignKey('users.user_id')),
                                db.Column('tracker_id', db.Integer, db.ForeignKey('trackers.id')))


class User(db.Model, UserMixin):
	__tablename__ = 'users'

	user_id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(255), unique=True, nullable=False)
	last_name = db.Column(db.String(255), unique=True)
	# user_password = db.Column(db.String, nullable=False)
	password = db.Column(db.LargeBinary)

	email_id = db.Column(db.String(255), unique=True, nullable=False)
	joined = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
	public_trackers = db.relationship("Tracker", secondary=public_user_trackers, backref=db.backref("users"))
	journals = db.relationship("UserJournal", backref=db.backref("users"))

	def __repr__(self):
		return "<User %r>" % self.first_name

	def __getitem__(self, item):
		return self.__dict__[item]

	def __init__(self, **kwargs):
		for property, value in kwargs.items():

			if hasattr(value, '__iter__') and not isinstance(value, str):
				# the ,= unpack of a singleton fails PEP8 (travis flake8 test)
				value = value[0]

			if property == 'password':
				value = hash_pass(value)  # we need bytes here (not plain str)

			setattr(self, property, value)


@login_manager.user_loader
def user_loader(user_id):
	return User.query.filter_by(user_id=user_id).first()


@login_manager.request_loader
def request_loader(request):
	user_email = request.form.get('email_id')
	user = User.query.filter_by(email_id=user_email).first()
	return user if user else None


class TrackerType(db.Model):
	__tablename__ = 'tracker_types'

	type_id = db.Column(db.Integer, primary_key=True)
	definition = db.Column(db.Text, nullable=False)

	def __getitem__(self, item):
		return self.__dict__[item]


class Tracker(db.Model):
	__tablename__ = 'trackers'

	tracker_id = db.Column('id', db.Integer, primary_key=True, unique=True)
	name = db.Column(db.Text, nullable=False)
	created_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
	units = db.Column(db.Text, nullable=False)
	tracker_type = db.Column(db.Integer, db.ForeignKey('tracker_types.type_id'), nullable=False)
	public = db.Column(db.Boolean, default=True)
	last_modified = db.Column(db.DateTime, nullable=True, default=None)
	description = db.Column(db.Text)
	custom_values = db.relationship('CustomEvent', backref='trackers')
	num_logs = db.relationship('NumLogger', backref='trackers')
	cat_logs = db.relationship('CatLogger', backref='trackers')

	def __getitem__(self, item):
		return self.__dict__[item]


class CustomEvent(db.Model):
	__tablename__ = 'custom_events'
	value_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
	tracker_id = db.Column('tracker_id', db.Integer, db.ForeignKey('trackers.id'), nullable=False)
	value_name = db.Column(db.Text, nullable=False)
	value_description = db.Column(db.Text)

	def __getitem__(self, item):
		return self.__dict__[item]


class NumLogger(db.Model):
	__tablename__ = 'numerical_logger'
	log_id = db.Column(db.Integer, primary_key=True, unique=True)
	created_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
	value = db.Column(db.Float, nullable=False)
	note = db.Column(db.Text)
	# discrete_value = db.Column(db.Integer, db.ForeignKey('custom_events.value_id'), nullable=True)
	tracker_id = db.Column(db.ForeignKey('trackers.id'), nullable=False)
	user = db.Column(db.ForeignKey('users.user_id'), nullable=False)

	def __getitem__(self, item):
		return self.__dict__[item]


class CatLogger(db.Model):
	__tablename__ = 'discrete_logger'
	log_id = db.Column(db.Integer, primary_key=True, unique=True)
	added_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
	# value = db.Column(db.Integer, nullable=False)
	note = db.Column(db.Text)
	value = db.Column('value_id', db.Integer, db.ForeignKey('custom_events.value_id'), nullable=False)
	tracker_id = db.Column(db.ForeignKey('trackers.id'), nullable=False)
	user = db.Column(db.ForeignKey('users.user_id'), nullable=False)

	def __getitem__(self, item):
		return self.__dict__[item]


class UserJournal(db.Model):
	__tablename__ = 'user_journal'
	journal_id = db.Column(db.Integer, primary_key=True, unique=True)
	journal_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
	entry = db.Column(db.Text, nullable=False)
	user = db.Column(db.ForeignKey('users.user_id'), nullable=False)

	def __getitem__(self, item):
		return self.__dict__[item]
