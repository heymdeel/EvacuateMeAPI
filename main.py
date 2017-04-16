import os
from flask import Flask
from loginAPI import login_api
from testAPI import test_api
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from utils import clean_sms_codes


scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=clean_sms_codes,
    trigger=IntervalTrigger(seconds=60),
    id='clean_codes',
    name='clean sms codes every minute',
    replace_existing=True)

app = Flask(__name__)
app.register_blueprint(login_api)
app.register_blueprint(test_api)
atexit.register(lambda: scheduler.shutdown())


@app.route('/')
def start():
    return 'Hello from DCP team'


if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
    #app.run(debug=True)
