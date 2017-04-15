from models import *
from utils import generate_hash


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
    key = generate_hash(args['login'], args['password'])
    Companies(name=args['name'],
              description=args['description'],
              address=args['address'],
              contact_phone=args['contact_phone'],
              email=args['email'],
              min_sum=args['min_sum'],
              tariff=args['tariff'],
              logo_url=args['logo_url'],
              login=args['login'],
              password=args['password'],
              api_key=key,
              sum_rate=0,
              count_rate=0)
    return key
