from flask import Blueprint, request, jsonify
from models import *
from google_maps import make_request_to_google, get_distance, get_duration

order_api = Blueprint('order_api', __name__)


@order_api.route('/api/help/companies', methods=['POST'])
@db_session
def list_of_companies():
    if 'api_key' not in request.headers:
        return 'Access refused! Need authorization via api_key', 401

    api_key = request.headers['api_key']
    if not Clients.exists(lambda c: c.api_key == api_key):
        return 'Access refused! api_key is wrong', 401

    req_json = request.get_json()
    client_lat = req_json['latitude']
    client_long = req_json['longitude']
    client_car_type = req_json['car_type']

    companies = []
    for worker in Workers.select(lambda w: w.status.id == 1 and w.supported_car_type.id == client_car_type): #find matching workers
        worker_location = Workers_last_location.get(worker=worker)
        result = make_request_to_google(client_lat, client_long, worker_location.latitude, worker_location.longitude)
        distance = get_distance(result)
        duration = get_duration(result)

        company_in_list = False
        for c in companies:
            if c['id'] == worker.company.id: #if company is already in list check for new minimal distance
                if distance < c['closest_distance']:
                    c['closest_distance'] = distance
                    c['closest_duration'] = duration
                company_in_list = True
                break

        if not company_in_list: #add new company to list
            company = worker.company.to_dict(exclude=['login', 'password', 'address', 'contact_phone', 'email',
                                                      'api_key', 'sum_rate', 'count_rate'])

            if worker.company.count_rate != 0:
                company['rate'] = worker.company.sum_rate / worker.company.count_rate
            else:
                company['rate'] = 0

            company['closest_distance'] = distance
            company['closest_duration'] = duration
            companies.append(company)

    if not companies:
        return '', 404

    companies.sort(key=lambda x: x['closest_distance'])
    return jsonify(companies), 200
