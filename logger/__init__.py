from flask import Blueprint

logger_bp = Blueprint('logger_bp', __name__)

from . import routes
