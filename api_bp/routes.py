from flask import jsonify, make_response
from flask_restful import Api, Resource, reqparse

from . import api_bp
from .RequestParsers import tracker_editor, specific_tracker_editor, tracker_creator, add_num_log, check_tracker_id, \
	check_user_id
from QuantSelf.logger.tools import LoggerDAO
from QuantSelf.models import User, CatLogger, NumLogger, db
from QuantSelf.tracker.tools import TrackerDAO

api = Api(api_bp)


class UserDetails(Resource):
	def get(self, user_id: int):
		_user: User = User.query.get(user_id)
		return jsonify(First_Name=_user.first_name, Last_Name=_user.last_name, Joined_Date=_user.joined)


_tracker: TrackerDAO = TrackerDAO()


class TrackerHelper(Resource):
	def get(self, tracker_id):
		if _tracker.exist(tracker_id) is False:
			return make_response(jsonify(error="This tracker ID doesn't exist"), 404)
		return _tracker.get_info(tracker_id)

	def delete(self, tracker_id):
		if _tracker.exist(tracker_id) is False:
			return make_response(jsonify(error="This tracker ID doesn't exist"), 404)
		else:
			status = _tracker.delete(tracker_id)
		return make_response(status, 200)

	def put(self, tracker_id):
		"""
		updating a tracker using the put statement and giving it relevant info.
		:return: success.
		"""
		if _tracker.exist(tracker_id) is False:
			return make_response(jsonify(error="This tracker ID doesn't exist"), 404)
		updated_data: dict[str] = specific_tracker_editor.parse_args()
		_updated_data, changes, rows = _tracker.update_info(tracker_id, updated_data)
		status = f'given_data_to_update :{_updated_data}\n' \
		         f'changes: {changes} \n' \
		         f'rows: {rows} '
		return make_response(status, 200)


class TrackerDB(Resource):
	def get(self):
		all_trackers = _tracker.__info__()
		return jsonify(all_trackers)

	def post(self):
		payload = tracker_creator.parse_args()
		tracker_type = payload['tracker_type']
		if tracker_type == 2 and payload['custom_values'] is None:
			return make_response(jsonify(error="This tracker needs custom categories for it to work"), 404)
		else:
			_tracker.create_tracker(payload)

	def put(self):
		"""
		updating a tracker using the put statement and giving it relevant info.
		:return: success.
		"""
		__tracker = TrackerDAO()
		new_tracker_data = tracker_editor.parse_args()
		tracker_id = new_tracker_data.pop('tracker_id')
		if __tracker.exist(tracker_id) is False:
			return make_response(jsonify(error="This tracker ID doesn't exist"), 404)
		updated_data: dict[str] = new_tracker_data
		_updated_data, changes, rows = __tracker.update_info(tracker_id, updated_data)
		status = f'given_data_to_update :{_updated_data}\n' \
		         f'changes: {changes} \n' \
		         f'rows: {rows} '
		return make_response(status, 200)


class LogHelper(Resource):
	def __init__(self):
		self.add_cat_log = add_num_log.copy()

	def get(self, user_id, tracker_id):
		__logger = LoggerDAO(user_id, tracker_id)
		if __logger.discrete:
			return __logger.get_cat_logs()

		else:
			return __logger.get_num_logs()

	def put(self, user_id, tracker_id):
		__logger = LoggerDAO(user_id, tracker_id)
		# edit_num_log.remove_argument('created_time')
		if __logger.discrete:
			# log_edits only contain value, note and created_time
			self.edit_cat_log = self.add_cat_log.copy()
			# self.edit_cat_log.remove_argument('tracker_id')
			# self.edit_cat_log.remove_argument('user')
			self.edit_cat_log.add_argument('log_id', type=__logger.check_log_id_for_editing, required=True)
			log_edits = self.edit_cat_log.parse_args()
			log_id = log_edits.pop('log_id')
			CatLogger.query.filter_by(log_id=log_id).update(**log_edits)
			db.session.commit()
		else:
			edit_num_log = add_num_log.copy()
			# edit_num_log.remove_argument('tracker_id')
			# edit_num_log.remove_argument('user')
			edit_num_log.add_argument('log_id', type=__logger.check_log_id_for_editing, required=True)
			log_edits = edit_num_log.parse_args()
			log_id = log_edits.pop('log_id')
			NumLogger.query.filter_by(log_id=log_id).update(**log_edits)
			db.session.commit()




	def delete(self, user_id, tracker_id):
		__logger = LoggerDAO(tracker_id, user_id)
		self.delete_log = reqparse.RequestParser(bundle_errors=True)
		self.delete_log.add_argument('log_id', type=__logger.check_log_id_for_editing, required=True)

		if __logger.discrete:
			waste = self.delete_log.parse_args()
			cl = CatLogger.query.get(waste['log_id'])
			db.session.delete(cl)
			db.session.commit()
		else:
			waste = self.delete_log.parse_args()
			nl = NumLogger.query.get(waste['log_id'])
			db.session.delete(nl)
			db.session.commit()


class CreateLog(LogHelper):
	def post(self, user_id, tracker_id):
		__logger = LoggerDAO(user_id, tracker_id)
		self.add_cat_log.replace_argument('value', type=__logger.check_custom_val_for_tracker)
		if check_user_id(user_id) is False or check_tracker_id(tracker_id) is False:
			raise ValueError("There is something wrong with the user_id or tracker_id supplied.")
		__logger = LoggerDAO(tracker_id, user_id)
		if __logger.discrete:
			new_log_data = self.add_cat_log.parse_args()
			new_log_data['tracker_id'] = tracker_id
			new_log_data['user'] = user_id
			new_log = CatLogger(**new_log_data)
			db.session.add(new_log)
			db.session.commit()
			return make_response("added", 200)
		else:
			new_log_data = add_num_log.parse_args()
			new_log = NumLogger(**new_log_data)
			db.session.add(new_log)
			db.session.commit()
			return make_response("added", 200)

api.add_resource(UserDetails, '/user/<int:user_id>')
api.add_resource(TrackerDB, '/trackers')
api.add_resource(TrackerHelper, '/trackers/<int:tracker_id>')
api.add_resource(LogHelper, '/user/<int:user_id>/trackers/<int:tracker_id>/logs')
api.add_resource(CreateLog, 'user/tracker/log/create')
