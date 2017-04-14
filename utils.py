from models import *
from models import *
import hashlib
import datetime
import re

def client_key_is_valid(req):
    if 'key' in req.headers and Clients.exists(lambda c: c.api_key.key == req.headers['key']):
        return True
    return False


def validate_phone(phone):
    if not (re.match(r'[7-8][0-9]{10}', phone) and len(phone) == 11):
        return False
    return True


def create_code_response(phone, code):
    return 'http://smsc.ru/sys/send.php?login=Debian17&psw=qwerty12&charset=utf-8&phones={0}&mes=Ваш код активации:{1}'\
        .format(phone, str(code))


def renew_code(phone, code):
    SMS_codes.get(lambda s: s.phone == phone and s.code == code).delete()
    hash_key = hashlib.md5(str(code).encode() + phone.encode())
    api_key = hash_key.hexdigest()
    return api_key


@db_session
def clean_sms_codes():
    delete(sms_code for sms_code in SMS_codes if datetime.datetime.now() - datetime.timedelta(minutes=5) > sms_code.time_stamp)