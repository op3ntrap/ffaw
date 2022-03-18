from flask_restful import Api, Resource
from flask import jsonify
from . import api_bp
# noinspection PyUnresolvedReferences
from QuantSelf.models import User, Tracker, TrackerType

api = Api(api_bp)


class UserDetails(Resource):
	def get(self, user_id: int):
		_user: User = User.query.get(user_id)
		return jsonify(First_Name=_user.first_name, Last_Name=_user.last_name, Joined_Date=_user.joined)


class TrackerHelper(Resource):
	def get(self, tracker_id):
		_tracker: Tracker = Tracker.query.get(tracker_id)
		if _tracker.public:
			subscribers = [f'{subscriber.first_name} {subscriber.last_name}' for subscriber in _tracker.public_users]
		else:
			subscribers = [f'{subscriber.first_name} {subscriber.last_name}' for subscriber in _tracker.private_users]
		if _tracker.tracker_type != 1:
			return jsonify(
				name=_tracker.name,
				created_time=_tracker.created_time,
				units=_tracker.units,
				tracker_type=_tracker.tracker_type,
				public=bool(_tracker.public),
				custom_values=[custom_value.name for custom_value in _tracker.custom_values],
				total_users=len(subscribers)
			)
		return jsonify(
			name=_tracker.name,
			created_time=_tracker.created_time,
			units=_tracker.units,
			tracker_type=_tracker.tracker_type,
			public=bool(_tracker.public),
			total_users=len(subscribers)
		)


api.add_resource(UserDetails, '/user/<int:user_id>')
api.add_resource(TrackerHelper, '/tracker/<int:tracker_id>')
