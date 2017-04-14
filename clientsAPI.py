from flask import Blueprint, jsonify, make_response, request
from models import *
import random
import grequests
from sms import *
from datetime import datetime
from reg_exp import *


clients_api = Blueprint('clients_api', __name__)
clients_api.add_app_url_map_converter(RegexConverter, 'regex')


@clients_api.route('/api/clients/verification/<regex("7[0-9]{11}"):phone>')
@db_session
def verificate(phone):
    if Clients.exists(lambda c: c.phone == phone):
        return '', 200
    return 'user was not found', 404


@clients_api.route('/api/clients/code/<regex("7[0-9]{11}"):phone>')
@db_session
def get_code(phone):
    code = random.randint(1000, 9999)
    SMS_codes(phone=phone, code=code, time_stamp=datetime.now())
    r = create_code_response(phone, code)
    urls = [r]
    rs = (grequests.post(u) for u in urls)
    grequests.map(rs)
    return '', 200


@clients_api.route('/api/clients', methods=['POST'])
@db_session
def sign_up():
    req = request.get_json()
    if SMS_codes.exists(lambda s: s.phone == req['phone'] and s.code == req['code']):
        new_key = renew_code(req['phone'], req['code'])
        key = Keys(key=new_key, role=Roles.get(name='Client'))
        Clients(name=req['name'], phone=req['phone'], api_key=key)
        return new_key, 201
    return 'sms time was out', 404


@clients_api.route('/api/clients/api_key')
@db_session
def sign_in():
    if 'phone' in request.headers and 'code' in request.headers:
        phone = request.headers['phone']
        code = request.headers['code']
        if SMS_codes.exists(lambda s: s.phone == phone and s.code == code):
            new_key = renew_code(phone, code)
            Clients.get(phone=phone).api_key.key = new_key
            return new_key, 200
        return 'sms time was out', 404
    return 'missing phone and sms-code', 400


@clients_api.route('/api/help/companies', methods=['POST'])
@db_session
def call_help():
    if code_is_valid(request):
        companies = []
        for c in Companies.select():
            companies.append(c.to_dict())
            return jsonify(companies), 200
    return '', 401


@clients_api.route('/api/orders/<string:company_name>', methods=['POST'])
@db_session
def place_order(company_name):
    if code_is_valid(request):
        return 'in construction', 200
