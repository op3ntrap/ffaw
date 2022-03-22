from ..models import CatLogger, NumLogger, Tracker, User, db


class LoggerDAO:
	def __init__(self, tracker_id, user_id):
		self.logs = None
		self.__tracker__: Tracker = Tracker.query.get(tracker_id)
		self.__user__: User = User.query.get(user_id)
		self.discrete = True if self.__tracker__.tracker_type == 2 else False
		self.permissible_values = []
		if self.discrete:
			self.logger = CatLogger
			self.permissible_values = {
				_cv.value_name: _cv.value_id for _cv in self.__tracker__.custom_values
			}
		else:
			self.logger = NumLogger

	def return_custom_val(self, value):
		records = {_cv.value_id: _cv.value_name for _cv in self.__tracker__.custom_values}
		return records[value]

	def edit_number_log(self, log_id, data):
		# if self.discrete:
		# log = self.logger(**dat
		# Check for valid log_id exists externally
		for key in data:
			if data[key] is None:
				data.pop(key)
		_log = NumLogger.query.filter_by(log_id=log_id).update(**data)
		db.session.commit()

	def get_cat_logs(self):
		self.logs: list[CatLogger] = CatLogger.query.filter_by(tracker_id=self.__tracker__.tracker_id,
		                                                       user=self.__user__.user_id)
		result = []
		for log in self.logs:
			result.append({
				'log_id'      : log.log_id,
				'user_id'     : log.user,
				'tracker_id'  : log.tracker_id,
				'created_time': log.created_time.strftime("%m/%d/%Y, %H:%M:%S"),
				'notes'       : log.notes,
				'value'       : self.return_custom_val(log.value)
			})
		return result

	def get_num_logs(self):
		self.logs: list[NumLogger] = NumLogger.query.filter_by(tracker_id=self.__tracker__.tracker_id,
		                                                       user=self.__user__.user_id)
		result = []
		for log in self.logs:
			result.append({
				'log_id'      : log.log_id,
				'user_id'     : log.user,
				'tracker_id'  : log.tracker_id,
				'created_time': log.created_time.strftime("%m/%d/%Y, %H:%M:%S"),
				'notes'       : log.note,
				'value'       : log.value
			})
		return result

	def check_log_id_for_editing(self, value):
		tracker_id = self.__tracker__.tracker_id,
		user = self.__user__.user_id
		__Numlogger = NumLogger.query.filter_by(tracker_id=tracker_id, user=user, log_id=value)
		__Catlogger = CatLogger.query.filter_by(tracker_id=tracker_id, user=user, log_id=value)
		_t: Tracker = Tracker.query.get(tracker_id)
		if _t.tracker_type == 2:
			if __Catlogger is None:
				raise ValueError(f'The parameter {value} given is not a valid log_id')
			else:
				return value
		else:
			if __Numlogger is None:
				raise ValueError(f'The parameter {value} given is not a valid log_id')
			else:
				return value

	def delete_log(self):
		if self.discrete:
			pass
		else:
			pass

	def check_custom_val_for_tracker(self, value):
		records = {_cv.value_name: _cv.value_id for _cv in self.__tracker__.custom_values}
		if value not in list(records.keys()):
			raise ValueError("Please enter valid input for the value.")
		return records[value]
