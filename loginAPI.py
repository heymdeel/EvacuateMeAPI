from flask import Blueprint, jsonify, make_response, request
from models import *
import random
import grequests
from utils import *
from datetime import datetime
import werkzeug.exceptions
from dbhelper import create_company

login_api = Blueprint('clients_api', __name__)


@login_api.route('/api/clients/verification/<string:phone>') #verificate if user with this phone number exists
@db_session
def verificate(phone):
    if not validate_phone(phone):
        return 'bad phone format', 400
    if Clients.exists(lambda c: c.phone == phone):
        return 'ok', 200
    return 'client was not found', 404


@login_api.route('/api/code/<string:phone>') #request for sending sms to user
@db_session
def get_code(phone):
    if not validate_phone(phone):
        return 'bad phone format', 400
    code = random.randint(1000, 9999)
    r = create_code_response(phone, code)
    urls = [r]
    rs = (grequests.post(u) for u in urls)
    if SMS_codes.exists(phone=phone):
        SMS_codes.get(phone=phone).set(code=code, time_stamp=datetime.now())
    else:
        SMS_codes(phone=phone, code=code, time_stamp=datetime.now())
    #grequests.map(rs)
    return 'ok', 200


@login_api.route('/api/clients', methods=['POST']) #register new user
@db_session
def sign_up():
    req = request.get_json()
    if not validate_phone(req['phone']):
        return 'bad phone format', 400
    if SMS_codes.exists(lambda s: s.phone == req['phone'] and s.code == req['code']):
        new_key = renew_code(req['phone'], req['code'])
        Clients(name=req['name'], phone=req['phone'], api_key=new_key)
        return new_key, 201
    return 'sms time was out or code is invalid', 404


@login_api.route('/api/clients/api_key') #get api_key for sign in
@db_session
def sign_in():
    if 'phone' in request.headers and 'code' in request.headers:
        phone = request.headers['phone']
        code = request.headers['code']
        if not validate_phone(phone):
            return 'bad phone format', 400
        if SMS_codes.exists(lambda s: s.phone == phone and s.code == code):
            new_key = renew_code(phone, code)
            Clients.get(phone=phone).api_key = new_key
            return new_key, 200
        return 'sms time was out', 404
    return 'missing phone or sms-code', 400


@login_api.route('/api/companies', methods=['POST']) #register new company
@db_session
def register_company():
    req_json = request.get_json()
    try:
        key = create_company(req_json)
    except Exception as e:
        return 'Failed to create company. Error message: ' + str(e), 400
    return key, 201
