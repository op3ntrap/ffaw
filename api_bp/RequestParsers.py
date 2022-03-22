from flask_restful import reqparse, inputs
from QuantSelf.models import Tracker, NumLogger, CatLogger
from QuantSelf.tracker.tools import TrackerDAO
from QuantSelf.auth.tools import UserDAO
from QuantSelf.logger.tools import LoggerDAO

__user = UserDAO()
__tracker = TrackerDAO()

tracker_id_choices = __tracker.available_public_trackers


def check_log_id(value, tracker_id, user_id):
	__Numlogger = NumLogger.query.filter_by(tracker_id=tracker_id, user_id=user_id, log_id=value)
	__Catlogger = CatLogger.query.filter_by(tracker_id=tracker_id, user_id=user_id, log_id=value)
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


def check_user_id(value):
	if type(value) != int or __user.exist(value) is False:
		raise ValueError(f'The parameter {value} given is not a valid user_id')
	return value


def check_tracker_id(value):
	if type(value) != int or __tracker.exist(value) is False:
		raise ValueError(f'The parameter {value} given is not a valid tracker_id')
	return value


def custom_event_value(value):
	if type(value) != str or value.count("|") > 1:
		raise ValueError(f'The parameter is not a string. If it is then it contains more than one | '
		                 f'separators.')
	if "|" in value:
		return {'value_name'       : value.split("|")[0],
		        'value_description': value.split("|")[1]}
	return {'value_name': value}


# tracker_id_choices = Tracker.current_tracker_ids()

# Public Tracker Editor from the /trackers endpoint
tracker_editor = reqparse.RequestParser(bundle_errors=True)
tracker_editor.add_argument('tracker_id',
                            type=int,
                            required=True,
                            choices=tracker_id_choices,
                            help='Please enter a valid integer for tracker_id')
tracker_editor.add_argument('name', type=str)
tracker_editor.add_argument('description', type=str, dest='description')
tracker_editor.add_argument('units', dest='units', type=str, help="Please enter the units as a string")
tracker_editor.add_argument('tracker_type', dest='tracker_type', type=int, choices=(1, 2, 3, 4),
                            help="Enter an integer from [1,4] , 1=[Numerical] , 2=[Categorical] , 3=[Boolean] , "
                                 "4=[Range]")
tracker_editor.add_argument('custom_values',
                            type=custom_event_value,
                            help="Format for entering a new categorical value is "
                                 "<category_name>|<category_description> \n eg.\n"
                                 "curl https://api.example.com -d 'add_category=bob|descr' -d "
                                 "'add_category=sue|descr -d "
                                 "'add_category=joe'",
                            action='append', store_missing=True, default=[])
tracker_editor.add_argument('delete_existing_custom_values', type=inputs.boolean, default=False, store_missing=True,
                            help="Assign True or False to this endpoint to delete all existing custom_values.")

# Create Public Tracker Editor for tracker specified through id.
specific_tracker_editor = tracker_editor.copy()
specific_tracker_editor.remove_argument('tracker_id')

# Create a New Public Tracker.
tracker_creator = reqparse.RequestParser(bundle_errors=True)
tracker_creator.add_argument('name', type=str, required=True, help="Please enter a valid name for your tracker")
tracker_creator.add_argument('tracker_type', type=int, choices=[1, 2, 3, 4], required=True,
                             help="Enter an integer from [1,4]  1=[Numerical], 2=[Categorical], 3=[Boolean],"
                                  " 4=[Range]")
tracker_creator.add_argument('units', required=True, type=str, help="Please enter the units as a string")
tracker_creator.add_argument('description', type=str, dest='description')
tracker_creator.add_argument('custom_values',
                             type=custom_event_value,
                             help="Format for entering a new categorical value is "
                                  "<category_name>|<category_description> \n eg.\n"
                                  "curl https://api.example.com -d 'add_category=bob|descr' -d "
                                  "'add_category=sue|descr -d "
                                  "'add_category=joe'. If the term doesn't contain |, a custom event without a "
                                  "description will be created.",
                             action='append', store_missing=True, default=[])

add_num_log = reqparse.RequestParser(bundle_errors=True)
# add_num_log.add_argument('tracker_id', type=int, help="Please enter a valid input", required=True)
# add_num_log.add_argument('user', type=int, help="Please enter a valid input", required=True)
add_num_log.add_argument('note', type=str, required=False, help="Add any remarks.")
add_num_log.add_argument('value', type=float, required=True, help="Please enter a valid value for the logger.")
add_num_log.add_argument('created_time', type=inputs.datetime_from_iso8601, help="Please enter time in the format of"
                                                                                 "YYYY-%M-%DT%H:%M:S", required=False)




