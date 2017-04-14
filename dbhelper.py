from models import *


@db_session
def create_from_json(args):
    Workers(name=args['name'], surname=args['surname'],
            patronymic=args['patronymic'], date_of_birth=args['date_of_birth'],
            date_of_hire=datetime.now(), status=Workers_status.get(id=0),
            phone=args['phone'])
