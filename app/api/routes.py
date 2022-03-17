from flask_restful import Api, Resource
from flask import Blueprint, current_app

api = Blueprint(__name__, "api", url_prefix="/api")
