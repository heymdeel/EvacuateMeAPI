import os
from flask import Flask
from loginAPI import login_api
from databaseAPI import database_api
from workerAPI import worker_api
from orderAPI import order_api
from web_site import web_site
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from utils import clean_sms_codes


#TODO: workers order history


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
app.register_blueprint(database_api)
app.register_blueprint(worker_api)
app.register_blueprint(order_api)
app.register_blueprint(web_site)
atexit.register(lambda: scheduler.shutdown())


@app.context_processor
def get_categories():
    categories = {}
    categories['Главная'] = '/'
    categories['Компании'] = '/companies'
    categories['О нас'] = '/about'

    return dict(categories=categories)


if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
    #app.run(debug=True)
