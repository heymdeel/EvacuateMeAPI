from flask import Blueprint, jsonify, make_response, request
from models import *
from datetime import datetime

help_api = Blueprint("help_api", __name__)

@help_api.route('api/kek')
@db.session
def kek():
    return 200