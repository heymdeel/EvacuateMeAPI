from flask import Blueprint, request, jsonify
from models import *
from datetime import datetime
from google_maps import make_request_to_google, get_distance

worker_api = Blueprint('worker_api', __name__)


@worker_api.route('/api/workers/status/<int:new_status>', methods=['PUT']) #change worker's status
@db_session
def change_status(new_status):
    if 'api_key' not in request.headers:
        return 'Access refused! Need authorization via api_key', 401

    api_key = request.headers['api_key']
    if not Workers.exists(lambda c: c.api_key == api_key):
        return 'Access refused! api_key is wrong', 401

    if not Workers_status.exists(lambda s: s.id == new_status):
        return 'Bad status number', 400

    try:
        Workers.get(api_key=api_key).set(status=new_status)
    except Exception as e:
        return 'Failed to change status. Error message: ' + str(e), 400

    return 'Status successfully changed to ' + Workers_status.get(id=new_status).description, 200


@worker_api.route('/api/workers/orders') #check for actual orders
@db_session
def check_for_orders():
    if 'api_key' not in request.headers:
        return 'Access refused! Need authorization via api_key', 401

    api_key = request.headers['api_key']
    if not Workers.exists(lambda c: c.api_key == api_key):
        return 'Access refused! api_key is wrong', 401

    order = Orders.get(worker=Workers.get(api_key=api_key), status=Orders_status.get(description='awaiting'))
    if order is None:
        return 'There is no actual orders for this worker ', 404

    client_info = {}
    client_info['latitude'] = order.start_client_lat
    client_info['longitude'] = order.start_client_long
    client_info['phone'] = order.client.phone
    client_info['order_id'] = order.id
    client_info['car_model'] = order.car_model
    client_info['car_colour'] = order.car_colour
    result = make_request_to_google(order.start_client_lat, order.start_client_long, order.start_worker_lat,
                                    order.start_worker_long)
    client_info['distance'] = get_distance(result)

    return jsonify(client_info), 200


@worker_api.route('/api/workers/location', methods=['PUT']) #change worker location
@db_session
def send_location():
    if 'api_key' not in request.headers:
        return 'Access refused! Need authorization via api_key', 401

    api_key = request.headers['api_key']
    if not Workers.exists(lambda c: c.api_key == api_key):
        return 'Access refused! api_key is wrong', 401

    worker = Workers.get(api_key=api_key)
    if worker.status.id == 0:
        return 'Worker is offline', 400

    req_json = request.get_json()
    new_latitude = req_json['latitude']
    new_longitude = req_json['longitude']

    try:
        Workers_location_history(worker=worker, latitude=new_latitude, longitude=new_longitude, time_stamp=datetime.now())
        last_location = Workers_last_location.get(worker=worker)

        if last_location is None:
            Workers_last_location(worker=worker, latitude=new_latitude, longitude=new_longitude)
        else:
            last_location.set(latitude=new_latitude, longitude=new_longitude)

    except Exception as e:
        return 'Failed to save location. Error message: ' + str(e), 400

    return 'Location was successfully saved', 200


@worker_api.route('/api/workers/<int:worker_id>/location') #get worker's current location
@db_session
def get_worker_location(worker_id):
    if 'api_key' not in request.headers:
        return 'Access refused! Need authorization via api_key', 401

    api_key = request.headers['api_key']
    if not Clients.exists(lambda c: c.api_key == api_key):
        return 'Access refused! api_key is wrong', 401

    worker = Workers.get(id=worker_id)
    if worker is None:
        return 'worker was not found', 404

    if worker.status.id == 0:
        return 'Worker is offline', 400

    worker_location = Workers_last_location.get(worker=worker)
    if worker_location is None:
        return '', 404

    response = {}
    response['latitude'] = worker_location.latitude
    response['longitude'] = worker_location.longitude

    return jsonify(response), 200


@worker_api.route('/api/workers/<int:id>/location/history') #get worker's location history
@db_session
def get_location_history(id):
    if 'api_key' not in request.headers:
        return 'Access refused! Need authorization via api_key', 401

    company = Companies.get(api_key=request.headers['api_key'])
    if company is None:
        return 'Access refused! api_key is wrong', 401

    worker = Workers.get(id=id)
    if worker not in company.workers:
        return 'There is no such worker in this company', 404

    location_history = Workers_location_history.select(lambda w: w.worker == worker)[:]
    if location_history is None:
        return 'There is no location history for this worker', 404

    result = []
    for i in location_history:
        result.append(i.to_dict(exclude=['worker', 'id']))

    return jsonify(result), 200
