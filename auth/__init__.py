from flask import Blueprint

auth_bp = Blueprint('authentication_blueprint', __name__, url_prefix='')

from . import routes
from . import errors
from . import forms
from . import views
