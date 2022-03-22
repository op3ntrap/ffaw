from ..models import Tracker, CustomEvent, TrackerType, db


# import dataclasses
def serialize_custom_event(_cv: CustomEvent):
	return {
		'value_id'         : _cv.value_id,
		'value_name'       : _cv.value_name,
		'value_description': _cv.value_description
	}


# @dataclasses
class TrackerDAO:

	def __init__(self):
		self.all_public_trackers = Tracker.query.filter_by(public=True)
		self.available_public_trackers: list[int] = [_t.tracker_id for _t in self.all_public_trackers]
		self.public = True
		self.data = {}

	def exist(self, tracker_id) -> bool:
		self.all_public_trackers = Tracker.query.filter_by(public=True)
		self.available_public_trackers: list[int] = [_t.tracker_id for _t in self.all_public_trackers]
		if tracker_id in self.available_public_trackers:
			return True
		return False

	@staticmethod
	def revise_tracker(tracker_id, changes):
		rows = Tracker.query.filter_by(tracker_id=tracker_id).update(changes)
		return rows

	@staticmethod
	def get_tracker_type(_type_id):
		_type: TrackerType = TrackerType.query.get(_type_id)
		return _type.definition

	@staticmethod
	def update_custom_events(tracker_id, events: list[dict[str]]):
		__tracker: Tracker = Tracker.query.get(tracker_id)
		current_custom_values = __tracker.custom_values
		current_custom_value_names = [cv.value_name for cv in __tracker.custom_values]
		new_events = []

		for _cv in events:
			if _cv['value_name'] in current_custom_value_names:
				rww = CustomEvent.query.filter_by(tracker_id=tracker_id, value_name=_cv['value_name']).update(_cv)
				db.session.commit()
			else:
				new_events.append(_cv)

		# Create if they don't exist
		for new_event in new_events:
			new_custom_value = CustomEvent(value_name=new_event['value_name'],
			                               value_description=new_event['value_description'])
			__tracker.custom_values.append(new_custom_value)
			db.session.commit()

	def get_info(self, tracker_id):
		__tracker: Tracker = Tracker.query.get(tracker_id)
		self.data = {'name'         : __tracker.name,
		             'description'  : __tracker.description,
		             'created_time' : __tracker.created_time.strftime("%m/%d/%Y, %H:%M:%S"),
		             'units'        : __tracker.units,
		             'tracker_type' : self.get_tracker_type(__tracker.tracker_type),
		             'last_modified': __tracker.last_modified.strftime("%m/%d/%Y, %H:%M:%S") if
		             __tracker.last_modified is not None else None,
		             'custom_values': []}
		if __tracker.tracker_type not in [1, 3]:
			_cvs = __tracker.custom_values
			for _cv in _cvs:
				self.data['custom_values'].append(serialize_custom_event(_cv))
		return self.data

	def update_info(self, tracker_id, _updated_data):
		# make updates to a tracker in its core properties
		changes = {}
		for key in _updated_data:
			if _updated_data[key] is None or key == 'custom_values' or key == 'delete_existing_custom_values' or key \
					== 'tracker_id':
				continue
			else:
				changes[key] = _updated_data[key]
		rows = self.revise_tracker(tracker_id, changes)
		db.session.commit()
		# delete custom events if enabled.
		if _updated_data['delete_existing_custom_values']:
			__tracker: Tracker = Tracker.query.get(tracker_id)
			_cvs = __tracker.custom_values
			for _c in _cvs:
				db.session.delete(_c)
				db.session.commit()
		# update custom events accordingly or create them.
		if _updated_data['custom_values']:
			self.update_custom_events(tracker_id, _updated_data['custom_values'])
		return _updated_data, changes, rows

	def __info__(self):
		self.all_public_trackers = Tracker.query.filter_by(public=True)
		self.available_public_trackers: list[int] = [_t.tracker_id for _t in self.all_public_trackers]
		return [self.get_info(_t_id) for _t_id in self.available_public_trackers]

	def create_tracker(self, payload):
		custom_events = payload.pop('custom_values')
		new_tracker = Tracker(**payload)
		db.session.add(new_tracker)
		# noinspection PySimplifyBooleanCheck
		if custom_events != []:
			for new_event in custom_events:
				new_custom_value = CustomEvent(value_name=new_event['value_name'],
				                               value_description=new_event['value_description'])
				new_tracker.custom_values.append(new_custom_value)
		db.session.commit()

	@staticmethod
	def delete(tracker_id):
		__tracker: Tracker = Tracker.query.get(tracker_id)
		db.session.delete(__tracker)
		db.session.commit()
		return "Completed"

	def tracker_custom_values(self, tracker_id):
		tracker_custom_values = []
		trckr:  Tracker = Tracker.query.get(tracker_id)
		return trckr.custom_values
