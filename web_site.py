from flask import Blueprint, render_template


web_site = Blueprint('web_site', __name__)


@web_site.route('/')
def index():
    return render_template('index.html', page='Главная', title='EvacuateMe')


@web_site.route('/companies')
def get_companies():
    return render_template('companies.html', title='Компании', page='Компании')


@web_site.route('/about')
def about_us():
    return render_template('about.html', tittle='О нас', page='О нас')