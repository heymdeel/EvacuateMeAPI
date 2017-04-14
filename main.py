import os
from models import *
from flask import Flask
from clientsAPI import clients_api
from helpAPI import help_api
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

app = Flask(__name__)
app.register_blueprint(clients_api)
app.register_blueprint(help_api)
atexit.register(lambda: scheduler.shutdown())


def clean_sms_codes():
    delete(sms_code for sms_code in SMS_codes if datetime.now - datetime.timedelta(minutes=10) > sms_code.time_stamp)

scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=clean_sms_codes,
    trigger=IntervalTrigger(seconds=15),
    id='clean_codes',
    name='clean sms codes every minute',
    replace_existing=True)


@app.route('/')
def start():
    return 'Hello from DCP team'


if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
    #app.run(debug=True)