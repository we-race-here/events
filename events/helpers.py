import base64
import datetime
import os
import random
import string
import uuid

import pyotp
from django.utils.dateparse import parse_datetime


def random_id(n=8, no_upper=False, no_lower=False, no_digit=False):
    rand = random.SystemRandom()
    chars = ''
    if no_upper is False:
        chars += string.ascii_uppercase
    if no_lower is False:
        chars += string.ascii_lowercase
    if no_digit is False:
        chars += string.digits
    if not chars:
        raise Exception('chars is empty! change function args!')
    return ''.join([rand.choice(chars) for _ in range(n)])


def get_random_upload_path(upload_dir, filename):
    ext = filename.split('.')[-1]
    randid = random_id(n=8)
    filename = "{0}-{1}.{2}".format(uuid.uuid4(), randid, ext)
    return os.path.join(upload_dir, filename)


def get_member_verify_otp(member, salt=None):
    from django.conf import settings
    otp_key = settings.OTP_MEMBER_VERIFY_KEY
    length = settings.OTP_MEMBER_VERIFY_CODE_LENGTH
    interval = settings.OTP_MEMBER_VERIFY_INTERVAL
    if salt:
        otp_key = f'{otp_key}-{salt}'

    otp_key = f'{otp_key}-{member.pk}'
    b32_key = base64.b32encode(otp_key.encode('u8')).decode('u8')
    return pyotp.TOTP(b32_key, digits=length, interval=interval)


####################################################################
# coerce
####################################################################
def date_coerce(s):
    return (s and datetime.datetime.strptime(s, '%Y-%m-%d').date()) or None


def time_coerce(s):
    if not s:
        return None
    format = '%H:%M' if len(s.split(':')) == 2 else '%H:%M:%S'
    return datetime.datetime.strptime(s, format).time() or None


def datetime_coerce(s):
    return (s and parse_datetime(s)) or None


def integer_safe_coerce(v):
    return int(v) if (v or v == 0) else None


def float_safe_coerce(v):
    return float(v) if (v or v == 0) else None


def number_safe_coerce(v):
    return None if (not v and v != 0) else int(v) if isinstance(v, int) else float(v)
