from flask import Blueprint, request, jsonify
from models import *


worker_api = Blueprint('worker_api', __name__)


@worker_api.route('/api/workers/status/<string:new_status>', methods=['PUT']) #change worker's status
@db_session
def change_status(new_status):
    if 'api_key' not in request.headers:
        return 'access refused, need authorization via api_key', 401

    api_key = request.headers['api_key']
    if not Workers.exists(lambda c: c.api_key == api_key):
        return 'access refused, api_key is wrong', 401

    if not Workers_status.exists(lambda s: s.id == new_status):
        return 'bad status number', 400

    try:
        Workers.get(api_key=api_key).set(status=new_status)
    except Exception as e:
        return 'Failed to change status. Error message: ' + str(e), 400

    return 'status successfully changed to ' + Workers_status.get(id=new_status).description, 200


@worker_api.route('/api/workers/orders') #check for actual orders
@db_session
def check_for_orders():
    if 'api_key' not in request.headers:
        return 'access refused, need authorization via api_key', 401

    api_key = request.headers['api_key']
    if not Workers.exists(lambda c: c.api_key == api_key):
        return 'access refused, api_key is wrong', 401

    order = Orders.get(worker=Workers.get(api_key=api_key), status=Orders_status.get(description='awaiting'))
    if order is None:
        return 'there is no actual orders for this worker ', 404

    client_info = {}
    client_info['latitude'] = order.start_client_lat
    client_info['longitude'] = order.start_client_long
    client_info['phone'] = order.client.phone

    return jsonify(client_info), 200
