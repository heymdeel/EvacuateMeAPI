from flask import Blueprint, jsonify, make_response, request
from models import *
import random
import grequests
from sms import *
import utils
from datetime import datetime

workers_api = Blueprint('workers_api', __name__)


@workers_api.route('/api/workers', methods=['POST'])
@db_session
def sign_up():
    req = request.get_json()
    if utils.key_is_valid(request):
        
