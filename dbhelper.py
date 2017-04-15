from models import *
from utils import generate_hash, rand_str
from datetime import datetime


@db_session
def create_worker(key, args):
    Workers(name=args['name'],
            surname=args['surname'],
            patronymic=args['patronymic'],
            date_of_birth=args['date_of_birth'],
            date_of_hire=datetime.now(),
            status=Workers_status[0],
            phone=args['phone'],
            api_key='test',
            car_number=args['car_number'],
            company=Companies.get(lambda c: c.api_key.key == key),
            supported_car_type=Car_type[args['car_type']])


@db_session
def create_company(args):
    key = generate_hash(args['login'], rand_str(10))
    Companies(name=args['name'],
              description=args['description'],
              address=args['address'],
              contact_phone=args['contact_phone'],
              email=args['email'],
              min_sum=args['min_sum'],
              tariff=args['tariff'],
              logo_url=args['logo_url'],
              login=args['login'],
              password=generate_hash(args['password'], args['login']),
              api_key=key,
              sum_rate=0,
              count_rate=0)
    return key


@db_session
def create_worker(args, company):
    key = generate_hash(args['phone'], rand_str(10))
    Workers(name=args['name'],
            surname=args['surname'],
            patronymic=args['patronymic'],
            date_of_birth=datetime.strptime(args['date_of_birth'], "%d-%b-%Y"),
            date_of_hire=datetime.now(),
            phone=args['phone'],
            car_number=args['car_number'],
            supported_car_type=args['supported_car_type'],
            company=company,
            api_key=key,
            status=Workers_status.get(description='not working'))
    return key