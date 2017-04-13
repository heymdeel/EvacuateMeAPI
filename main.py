import os
from models import *
from flask import Flask
from clientsAPI import clients_api
from helpAPI import help_api

app = Flask(__name__)

app.register_blueprint(clients_api)
app.register_blueprint(help_api)

@app.route('/')
def start():
    return 'Hello, klac-klac'


if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    # app.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
    app.run(debug=True)
