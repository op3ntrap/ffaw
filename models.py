import datetime

from flask_sqlalchemy import SQLAlchemy
from flask import jsonify

# from . import app

db = SQLAlchemy()

public_user_trackers = db.Table('public_user_trackers',
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
	# private_trackers = db.relationship("Tracker", secondary=private_user_trackers, backref=db.backref("users"))
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
	custom_values = db.relationship('CustomEvent', backref=db.backref('trackers'))
	last_modified = db.Column(db.DateTime, nullable=True, default=None)

	@classmethod
	def serialize_tracker(cls):
		subscribers = [f'{subscriber.first_name} {subscriber.last_name}' for subscriber in cls.users]
		if cls.tracker_type != 1:
			return jsonify(
				name=cls.name,
				created_time=cls.created_time,
				units=cls.units,
				tracker_type=cls.tracker_type,
				public=bool(cls.public),
				custom_values=[custom_value.name for custom_value in cls.custom_values],
				total_users=len(subscribers)
			)
		return jsonify(
			name=cls.name,
			created_time=cls.created_time,
			units=cls.units,
			tracker_type=cls.tracker_type,
			public=bool(cls.public),
			total_users=len(subscribers)
		)

	@classmethod
	def current_tracker_ids(cls):
		_trackers = cls.query.all()
		current_ids = [_t.tracker_id for _t in _trackers]
		return current_ids


class Logger(db.Model):
	__tablename__ = 'logger'

	tracker = db.Column(db.ForeignKey('trackers.id'), nullable=False)
	user = db.Column(db.ForeignKey('users.user_id'), nullable=False)
	log_id = db.Column(db.Integer, primary_key=True, unique=True)
	added_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
	value = db.Column(db.Float, nullable=False)
	note = db.Column(db.Text)


class UserJournal(db.Model):
	__tablename__ = 'user_journal'

	journal_id = db.Column(db.Integer, primary_key=True, unique=True)
	journal_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
	entry = db.Column(db.Text, nullable=False)
	user = db.Column(db.ForeignKey('users.user_id'), nullable=False)


class CustomEvent(db.Model):
	__tablename__ = 'custom_events'

	value_id = db.Column(db.Integer, primary_key=True, unique=True)
	tracker_id = db.Column(db.ForeignKey('trackers.id'), nullable=False)
	value_name = db.Column(db.Text, nullable=False)
	value_description = db.Column(db.Text)
