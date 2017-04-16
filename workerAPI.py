from flask import Blueprint, request
from models import *


worker_api = Blueprint('worker_api', __name__)


@worker_api.route('/api/workers/status/<string:status>', methods=['PUT']) #change worker's status
@db_session
def change_status(status):
    if 'api_key' in request.headers:
        if not Workers.exists(lambda c: c.api_key == request.headers['api_key']):
            return 'access refused, api_key is wrong', 401
        if not Workers_status.exists(lambda s: s.id == status):
            return 'bad status number', 400
        try:
            Workers.get(api_key=request.headers['api_key']).set(status=status)
        except Exception as e:
            return 'Failed to change status. Error message: ' + str(e), 400
        return 'status successfully changed to ' + Workers_status.get(id=status).description, 200
    return 'access refused, need authorization via api_key', 401
