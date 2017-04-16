from flask import Blueprint, request
from models import *
import grequests
import random
from utils import *
from datetime import datetime
from dbhelper import create_company, create_worker

login_api = Blueprint('login_api', __name__)


#======================================|CLIENT|========================================================================
#======================================================================================================================


@login_api.route('/api/clients/verification/<string:phone>') #verificate if user with this phone number exists
@db_session
def clients_verification(phone):
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
def clients_sign_up():
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
def clients_sign_in():
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


#======================================|COMPANY|=======================================================================
#======================================================================================================================


@login_api.route('/api/companies', methods=['POST']) #register new company
@db_session
def company_sign_up():
    req_json = request.get_json()

    try:
        key = create_company(req_json)
    except Exception as e:
        return 'Failed to register company. Error message: ' + str(e), 400

    return key, 201


@login_api.route('/api/companies/login') #login company
@db_session
def company_sign_in():
    if 'login' in request.headers and 'password' in request.headers:
        login = request.headers['login']
        password = generate_password(login, 'some_salt' + request.headers['password'])

        if Companies.exists(lambda c: c.login == login and c.password == password):
            new_key = generate_hash('login', rand_str(10))
            Companies.get(login=login).api_key = new_key
            return new_key, 200
        return 'no such user with these login and password', 404

    return 'missing login or password', 400


#======================================|WORKER|========================================================================
#======================================================================================================================

@login_api.route('/api/workers', methods=['POST']) #register new worker
@db_session
def worker_sign_up():
    if 'api_key' not in request.headers:
        return 'access refused, need authorization via api_key', 401

    if not Companies.exists(lambda c: c.api_key == request.headers['api_key']):
        return 'access refused, api_key is wrong', 401

    company = Companies.get(api_key=request.headers['api_key'])
    req_json = request.get_json()

    try:
        key = create_worker(req_json, company)
    except Exception as e:
        return 'Failed to register worker. Error message: ' + str(e), 400

    return key, 201


@login_api.route('/api/workers/verification/<string:phone>') #verificate worker phone
@db_session
def workers_verification(phone):
    if not validate_phone(phone):
        return 'bad phone format', 400

    if Workers.exists(lambda c: c.phone == phone):
        return 'ok', 200

    return 'worker was not found', 404


@login_api.route('/api/workers/api_key') #get api_key for sign in
@db_session
def workers_sign_in():
    if 'phone' in request.headers and 'code' in request.headers:
        phone = request.headers['phone']
        code = request.headers['code']

        if not validate_phone(phone):
            return 'bad phone format', 400

        if SMS_codes.exists(lambda s: s.phone == phone and s.code == code):
            new_key = renew_code(phone, code)
            Workers.get(phone=phone).api_key = new_key
            return new_key, 200
        return 'sms time was out', 404

    return 'missing phone or sms-code', 400
