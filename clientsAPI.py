from flask import Blueprint, jsonify, make_response, request
from models import *
from datetime import datetime
import hashlib

clients_api = Blueprint('clients_api', __name__)


@clients_api.route('/api/clients/verification/<string:phone>')
@db_session
def verificate(phone):
    if Clients.exsists(lambda c: c.phone == phone):
        return 200
    return 404


@clients_api.route('/api/clients/code/<string:phone>')
@db_session
def get_code(phone):
    if Clients.exists(lambda c: c.phone == phone):
        code = random(1000, 9999)
        SMS_codes(phone=phone, code=code, time_stramp=datetime.now())
        return 200
    return 404


@clients_api.route('/api/clients>', methods=['POST'])
@db_session
def sign_up():
    req = request.get_json()
    if SMS_codes.exists(lambda s: s.phone == req['phone']
                        and s.code == req['code'])
        api_key = hashlib.md5(req['code'].encode() + req['phone'].encode())
        key = Keys(key=api_key.hexdigest(), role=Roles.get(name='Client'))
        return api_key, 201
