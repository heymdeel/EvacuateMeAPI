from pony.orm import *
from datetime import datetime

db = Database()


class SMS_codes(db.Entity):
    phone = Required(str, 11, unique=True)
    code = Required(int)
    time_stamp = Required(datetime)


class Clients(db.Entity):
    name = Required(str, 15)
    phone = Required(str, 11, unique=True)
    api_key = Required(str, unique=True)
    orders = Set('Orders')


class Companies(db.Entity):
    name = Required(str, 20)
    description = Required(str, 20)
    address = Required(str, 20)
    contact_phone = Required(str, 11, unique=True)
    email = Required(str, 25, unique=True)
    min_sum = Required(float)
    tariff = Required(float)
    sum_rate = Required(int)
    count_rate = Required(int)
    logo_url = Required(str, unique=True)
    login = Required(str, 15, unique=True)
    password = Required(str)
    api_key = Required(str, unique=True)
    workers = Set('Workers')


class Workers(db.Entity):
    name = Required(str, 15)
    surname = Required(str, 15)
    patronymic = Optional(str, 15)
    date_of_birth = Required(datetime)
    date_of_hire = Required(datetime)
    phone = Required(str, 11, unique=True)
    api_key = Required(str, unique=True)
    car_number = Required(str, 15, unique=True)
    company = Required(Companies)
    status = Required('Workers_status')
    location_history = Set('Workers_location_history')
    last_location = Optional('Workers_last_location')
    orders = Set('Orders')
    supported_car_type = Required('Car_type')


class Workers_status(db.Entity):
    description = Required(str, 20)
    workers = Set(Workers)


class Workers_location_history(db.Entity):
    worker = Required(Workers)
    latitude = Required(float)
    longitude = Required(float)
    time_stamp = Required(datetime)


class Workers_last_location(db.Entity):
    worker = PrimaryKey(Workers)
    latitude = Required(float)
    longitude = Required(float)


class Orders(db.Entity):
    client = Required(Clients)
    worker = Required(Workers)
    start_client_lat = Required(float)
    start_client_long = Required(float)
    start_worker_lat = Required(float)
    start_worker_long = Required(float)
    beginning_time = Required(datetime)
    termination_time = Optional(datetime)
    final_lat = Optional(float)
    final_long = Optional(float)
    commentary = Optional(str, 50)
    status = Required('Orders_status')
    car_type = Required('Car_type')


class Car_type(db.Entity):
    name = Required(str, 30)
    orders = Set(Orders)
    workers = Set(Workers)


class Orders_status(db.Entity):
    description = Required(str, 20)
    orders = Set(Orders)


db.bind('postgres', dbname="d3p9qhfg5eam1h", user="ngmdcklcqvatps",
        password="67483f8244dbd58058fe554618a87b33cd0dddfc5c7ad21fa3ace59c2e67c343",
        host='ec2-79-125-125-97.eu-west-1.compute.amazonaws.com', port='5432')
db.generate_mapping(create_tables=True)
