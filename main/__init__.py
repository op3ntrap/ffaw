from flask import Blueprint

main_bp = Blueprint('home_blueprint', __name__)

from . import routes
