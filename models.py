from pony.orm import *
from datetime import datetime

db = Database()

class SMS_codes(db.Entity):
    phone = Required(str, unique=True)
    code = Required(int)
    time_stramp = Required(datetime)


class Clients(db.Entity):
    name = Required(str)
    phone = Required(str, unique=True)
    api_key = Required('keys')
    orders = Set('orders')


class Companies(db.Entity):
    name = Required(str)
    description = Required(str)
    address = Required(str)
    contact_phone = Required(str)
    email = Required(str, unique=True)
    min_sum = Required(float)
    tariff = Required(float)
    sum_rate = Required(int)
    count_rate = Required(int)
    logo_url = Required(str)
    login = Required(str)
    password = Required(str)
    workers = Set('workers')
    api_key = Required('keys')


class Workers(db.Entity):
    name = Required(str)
    surname = Required(str)
    patronymic = Required(str)
    date_of_birth = Required(datetime)
    date_of_hire = Required(datetime)
    status = Required('workers_status')
    phone = Required(str)
    api_key = Required('keys')
    company = Required(companies)
    location_history = Set('workers_location_history')
    last_location = Optional('workers_last_location')
    orders = Set('orders')


class Workers_status(db.Entity):
    description = Required(str)
    workers = Set(workers)


class Workers_location_history(db.Entity):
    worker = Required(workers)
    latitude = Required(Decimal)
    longitude = Required(Decimal)
    time_stramp = Required(datetime)


class Workers_last_location(db.Entity):
    worker = Required(workers)
    latitude = Required(Decimal)
    longitude = Required(Decimal)


class Keys(db.Entity):
    key = Required(str)
    role = Required(str)
    clients = Set(clients)
    workers = Set(workers)
    companies = Set(companies)


class Orders(db.Entity):
    client = Required(clients)
    worker = Required(workers)
    start_client_lat = Required(Decimal)
    start_client_long = Required(Decimal)
    start_worker_lat = Required(Decimal)
    start_worker_long = Required(Decimal)
    begining_time = Required(datetime)
    termination_time = Optional(datetime)
    final_lat = Optional(Decimal)
    final_long = Optional(Decimal)
    status = Required('orders_status')


class Orders_status(db.Entity):
    description = Required(str)
    orders = Set(orders)


db.bind('postgres', dbname="d3p9qhfg5eam1h", user="ngmdcklcqvatps",
        password="67483f8244dbd58058fe554618a87b33cd0dddfc5c7ad21fa3ace59c2e67c343",
        host='ec2-79-125-125-97.eu-west-1.compute.amazonaws.com', port='5432')
db.generate_mapping(create_tables=True)
