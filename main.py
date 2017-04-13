from models import *
from flask import Flask

app = Flask(__name__)


@app.route('/')
def start():
    return 'Hello, klac-klac'


if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
    # app.run(debug=True)
