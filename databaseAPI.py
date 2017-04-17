from flask import Blueprint, jsonify
from models import *
from utils import rand_str, generate_password, generate_hash
from datetime import datetime

database_api = Blueprint('database_api', __name__)


@database_api.route('/api/car_types')
@db_session
def get_car_types():
    car_types = Car_type.select()[:]
    if car_types is None:
        return 'There is no car types in database', 404

    result = []
    for i in car_types:
        result.append(i.to_dict())

    return jsonify(result), 200

#==========================|DANGEROUS ZONE|=============================================================================
@database_api.route('/api/database/seed')
@db_session
def dangerous_method():
    Car_type(name='Легковая')
    Car_type(name='Грузовая')
    Workers_status(id=0, description='not working')
    Workers_status(id=1, description='working')
    Workers_status(id=2, description='performing order')
    Orders_status(id=0, description='awaiting')
    Orders_status(id=1, description='on the way')
    Orders_status(id=2, description='performing')
    Orders_status(id=3, description='completed')
    Orders_status(id=4, description='canceled by client')
    Orders_status(id=5, description='canceled by worker')

    #====================|company 1|========================================================
    key = generate_hash('company1', rand_str(10))
    Companies(id=1,
              name='ООО Эвакуатор',
              description='бюджетная компания',
              address='Текучева 132',
              contact_phone='79285548796',
              email='evacuator@gmail.com',
              min_sum=500,
              tariff=100,
              logo_url='https://raw.githubusercontent.com/reactjs/redux/master/logo/logo.png',
              login='company1',
              password=generate_password('company1', 'some_salt' + 'qwerty'),
              api_key=key,
              sum_rate=0,
              count_rate=0)

    key = generate_hash('79613202176', rand_str(10))
    Workers(name='Иван',
            surname='Павлов',
            patronymic='Петрович',
            date_of_birth=datetime.strptime('26-Sep-1849', "%d-%b-%Y"),
            date_of_hire=datetime.now(),
            phone='79613202176',
            car_number='о1488ру 161',
            supported_car_type=1,
            company=1,
            api_key=key,
            status=Workers_status.get(description='not working'))

    key = generate_hash('79782354687', rand_str(10))
    Workers(name='Андрей',
            surname='Сахаров',
            patronymic='Дмитриевич',
            date_of_birth=datetime.strptime('26-Sep-1849', "%d-%b-%Y"),
            date_of_hire=datetime.now(),
            phone='79782354687',
            car_number='о1482ру 161',
            supported_car_type=1,
            company=1,
            api_key=key,
            status=Workers_status.get(description='working'))
    Workers_last_location(worker=Workers.get(phone='79782354687'), latitude=47.29954729, longitude=39.72335458)

    key = generate_hash('79247896241', rand_str(10))
    Workers(name='Борис',
            surname='Пастернак',
            patronymic='Леонидович',
            date_of_birth=datetime.strptime('26-Sep-1849', "%d-%b-%Y"),
            date_of_hire=datetime.now(),
            phone='79247896241',
            car_number='о1481ру 161',
            supported_car_type=1,
            company=1,
            api_key=key,
            status=Workers_status.get(description='not working'))

    #====================|company 2|========================================================
    key = generate_hash('company2', rand_str(10))
    Companies(id=2,
              name='Мега Эвакуатор',
              description='недорогая компания',
              address='Ворошиловский 35',
              contact_phone='79523365478',
              email='mega_evacuator@gmail.com',
              min_sum=1000,
              tariff=150,
              logo_url='https://thumb7.shutterstock.com/display_pic_with_logo/3799943/566679331/stock-vector-evacuator-car-icon-isolated-on-white-background-evacuator-vector-logo-flat-design-style-modern-566679331.jpg',
              login='company2',
              password=generate_password('company2', 'some_salt' + 'qwerty'),
              api_key=key,
              sum_rate=0,
              count_rate=0)

    key = generate_hash('79265451223', rand_str(10))
    Workers(name='Виталий',
            surname='Гинзбург',
            patronymic='Лазаревич',
            date_of_birth=datetime.strptime('26-Sep-1849', "%d-%b-%Y"),
            date_of_hire=datetime.now(),
            phone='79265451223',
            car_number='о1483ру 161',
            supported_car_type=1,
            company=2,
            api_key=key,
            status=Workers_status.get(description='working'))
    Workers_last_location(worker=Workers.get(phone='79265451223'), latitude=47.30893968, longitude=39.72607434)

    key = generate_hash('79652234789', rand_str(10))
    Workers(name='Иван',
            surname='Бунин',
            patronymic='Алексеевич',
            date_of_birth=datetime.strptime('26-Sep-1849', "%d-%b-%Y"),
            date_of_hire=datetime.now(),
            phone='79652234789',
            car_number='о1484ру 161',
            supported_car_type=1,
            company=2,
            api_key=key,
            status=Workers_status.get(description='working'))
    Workers_last_location(worker=Workers.get(phone='79652234789'), latitude=47.32587958, longitude=39.74066019)

    key = generate_hash('79245687924', rand_str(10))
    Workers(name='Александр',
            surname='Солженицын',
            patronymic='Исаевич',
            date_of_birth=datetime.strptime('26-Sep-1849', "%d-%b-%Y"),
            date_of_hire=datetime.now(),
            phone='79245687924',
            car_number='о1485ру 161',
            supported_car_type=1,
            company=2,
            api_key=key,
            status=Workers_status.get(description='not working'))

    # ====================|company 3|========================================================
    key = generate_hash('company3', rand_str(10))
    Companies(id=3,
              name='Супер Эвакуатор',
              description='Дорогая компания',
              address='Вятская 44',
              contact_phone='79645589752',
              email='super_evacuator@gmail.com',
              min_sum=1500,
              tariff=200,
              logo_url='https://image.shutterstock.com/display_pic_with_logo/2539615/285667379/stock-vector--evacuator-icon-vector-285667379.jpg',
              login='company3',
              password=generate_password('company3', 'some_salt' + 'qwerty'),
              api_key=key,
              sum_rate=0,
              count_rate=0)

    key = generate_hash('79256431578', rand_str(10))
    Workers(name='Константин',
            surname='Новосёлов',
            patronymic='Сергеевич',
            date_of_birth=datetime.strptime('26-Sep-1849', "%d-%b-%Y"),
            date_of_hire=datetime.now(),
            phone='79256431578',
            car_number='о1486ру 161',
            supported_car_type=1,
            company=3,
            api_key=key,
            status=Workers_status.get(description='working'))
    Workers_last_location(worker=Workers.get(phone='79256431578'), latitude=47.30085694, longitude=39.74796653)

    key = generate_hash('79245678924', rand_str(10))
    Workers(name='Пётр',
            surname='Капица',
            patronymic='Леонидович',
            date_of_birth=datetime.strptime('26-Sep-1849', "%d-%b-%Y"),
            date_of_hire=datetime.now(),
            phone='79245678924',
            car_number='о1487ру 161',
            supported_car_type=1,
            company=3,
            api_key=key,
            status=Workers_status.get(description='working'))
    Workers_last_location(worker=Workers.get(phone='79245678924'), latitude=47.298485, longitude=39.78335023)

    key = generate_hash('79245678928', rand_str(10))
    Workers(name='Андрей',
            surname='Гейм',
            patronymic='Константинович',
            date_of_birth=datetime.strptime('26-Sep-1849', "%d-%b-%Y"),
            date_of_hire=datetime.now(),
            phone='79245678928',
            car_number='о1490ру 161',
            supported_car_type=1,
            company=3,
            api_key=key,
            status=Workers_status.get(description='not working'))
    return '', 200
