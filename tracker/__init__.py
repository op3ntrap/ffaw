from flask import Blueprint

tracker_bp = Blueprint('tracker_bp', __name__)

from . import routes
