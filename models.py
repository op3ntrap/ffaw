import datetime

from flask_sqlalchemy import SQLAlchemy

# from . import app

db = SQLAlchemy()

public_user_trackers = db.Table('public_user_trackers',
                                db.Column('user_id', db.Integer, db.ForeignKey('users.user_id')),
                                db.Column('tracker_id', db.Integer, db.ForeignKey('trackers.id')))

private_user_trackers = db.Table('private_user_trackers',
                                 db.Column('user_id', db.Integer, db.ForeignKey('users.user_id')),
                                 db.Column('tracker_id', db.Integer, db.ForeignKey('trackers.id')))


class User(db.Model):
	__tablename__ = 'users'

	user_id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(255), unique=True, nullable=False)
	last_name = db.Column(db.String(255), unique=True)
	user_password = db.Column(db.String, nullable=False)
	email_id = db.Column(db.String(255), unique=True, nullable=False)
	joined = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
	public_trackers = db.relationship("Tracker", secondary=public_user_trackers, backref=db.backref("users"))
	private_trackers = db.relationship("Tracker", secondary=private_user_trackers, backref=db.backref("users"))
	journals = db.relationship("UserJournal", backref=db.backref("users"))

	def __repr__(self):
		return "<User %r>" % self.first_name


class TrackerType(db.Model):
	__tablename__ = 'tracker_types'

	type_id = db.Column(db.Integer, primary_key=True)
	definition = db.Column(db.Text, nullable=False)


class Tracker(db.Model):
	__tablename__ = 'trackers'

	tracker_id = db.Column('id', db.Integer, primary_key=True, unique=True)
	name = db.Column(db.Text, nullable=False)
	created_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
	units = db.Column(db.Text, nullable=False)
	tracker_type = db.Column(db.ForeignKey('tracker_types.type_id'), nullable=False)
	public = db.Column(db.Boolean, default=True)
	public_users = db.relationship("User", secondary=public_user_trackers, backref=db.backref("trackers"))
	private_users = db.relationship("User", secondary=private_user_trackers, backref=db.backref("trackers"))
	custom_values = db.relationship('CustomEvent', backref=db.backref('trackers'))


class Logger(db.Model):
	__tablename__ = 'logger'

	tracker = db.Column(db.ForeignKey('trackers.id'), nullable=False)
	user = db.Column(db.ForeignKey('users.user_id'), nullable=False)
	log_id = db.Column(db.Integer, primary_key=True, unique=True)
	added_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
	value = db.Column(db.Float, nullable=False)
	note = db.Column(db.Text)

# tracker1 = db.relationship('Tracker')
# user1 = db.relationship('User')


class UserJournal(db.Model):
	__tablename__ = 'user_journal'

	journal_id = db.Column(db.Integer, primary_key=True, unique=True)
	journal_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
	entry = db.Column(db.Text, nullable=False)
	user = db.Column(db.ForeignKey('users.user_id'), nullable=False)

	user1 = db.relationship('User')


class CustomEvent(db.Model):
	__tablename__ = 'custom_events'

	value_id = db.Column(db.Integer, primary_key=True, unique=True)
	tracker_id = db.Column(db.ForeignKey('trackers.id'), nullable=False)
	value_name = db.Column(db.Text, nullable=False)
	value_description = db.Column(db.Text)
