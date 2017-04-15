from flask import Blueprint, jsonify, make_response, request
from models import *
import random
import grequests
from utils import *
from datetime import datetime

orders_api = Blueprint('orders_api', __name__)


@orders_api.route('/api/help/companies', methods=['POST'])
@db_session
def call_help():
    if client_key_is_valid(request):
        companies = []
        for c in Companies.select():
            companies.append(c.to_dict())
            return jsonify(companies), 200
    return '', 401


@orders_api.route('/api/orders/<string:company_name>', methods=['POST'])
@db_session
def place_order(company_name):
    if client_key_is_valid(request):
        return 'in construction', 200