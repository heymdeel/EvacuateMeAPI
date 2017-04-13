from flask import Blueprint

clients_api = Blueprint('clients_api', __name__)

@clients_api.route('/clients')
def clients():
    return 'Пшёл вон'
