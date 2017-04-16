from models import *
import hashlib
import datetime
import re
import random, string


def rand_str(length):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))


def validate_phone(phone):
    if not (re.match(r'[7-8][0-9]{10}', phone) and len(phone) == 11):
        return False
    return True


def create_code_response(phone, code):
    return 'http://smsc.ru/sys/send.php?login=Debian17&psw=qwerty12&charset=utf-8&phones={0}&mes=Ваш код активации:{1}'\
        .format(phone, str(code))


def generate_hash(arg1, arg2):
    hash_key = hashlib.md5(str(arg1).encode() + str(arg2).encode())
    return str(hash_key.hexdigest())


def generate_password(arg1, arg2):
    hash_pass = hashlib.sha512(str(arg1).encode() + str(arg2).encode())
    return str(hash_pass.hexdigest())


def renew_code(phone, code):
    SMS_codes.get(lambda s: s.phone == phone and s.code == code).delete()
    api_key = generate_hash(code, phone)
    return api_key


@db_session
def clean_sms_codes():
    delete(sms_code for sms_code in SMS_codes if datetime.datetime.now() - datetime.timedelta(minutes=5) > sms_code.time_stamp)