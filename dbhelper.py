from models import *


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
