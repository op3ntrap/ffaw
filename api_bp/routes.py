from flask_restful import Api, Resource, reqparse
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
	tracker_editor = reqparse.RequestParser(bundle_errors=True)
	tracker_editor.add_argument('tracker_id',
	                            type=int,
	                            required=True,
	                            choices=Tracker.current_tracker_ids(),
	                            help='Please enter a valid integer for tracker_id')
	tracker_editor.add_argument('units', type='str', help="Please enter the units as a string")
	tracker_editor.add_argument('tracker_type', type=int, choices=[1, 2, 3],
	                            help="Enter an integer from [1,3] \n 1=[Numerical] \n 2=[Categorical] \n 3=[Boolean]")
	tracker_editor.add_argument('public', type='boolean')
	tracker_editor.add_argument('name', type='str')

	def get(self, tracker_id):
		_tracker: Tracker = Tracker.query.get(tracker_id)
		tracker_detail = _tracker.serialize()
		return tracker_detail

	def put(self, tracker_id):
		pass

	def post(self, tracker_id):
		pass

	def delete(self, tracker_id):
		pass


class TrackerList(Resource):
	def get(self):
		_trackers = Tracker.query.all()
		tracker_list = [_t.serialze() for _t in _trackers]
		return jsonify(tracker_list)


api.add_resource(UserDetails, '/user/<int:user_id>')
api.add_resource(TrackerList, '/trackers')
api.add_resource(TrackerHelper, '/trackers/<int:tracker_id>')
