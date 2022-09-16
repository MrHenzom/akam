import json
import logging
import time

from flask import request, session

from .shared import DOOM_PATH
from .utils import InvalidCaptcha, contact_hook, get_user_ip, verify_captcha


# 30min
CONTACT_TIMEOUT = 30 * 60


class SendTimeout(Exception):
    pass


logger = logging.getLogger('debug')
logger.name = __name__


def get_doom_contact(user_ip):
    now = int(time.time())
    current_contact = None

    with open(DOOM_PATH) as f:
        dooms = json.load(f)

    new_dooms = []

    # [user_ip, timeout, email]
    for user_contact in dooms:
        if user_contact[0] == user_ip:
            current_contact = user_contact

        if user_contact[1] > now:
            new_dooms.append(user_contact)

    with open(DOOM_PATH, 'w') as f:
        json.dump(new_dooms, f, indent=4, )

    return current_contact


def add_doom_contact(info):

    with open(DOOM_PATH) as f:
        dooms = json.load(f)

    dooms.append(info)

    with open(DOOM_PATH, 'w') as f:
        json.dump(dooms, f)


def send_contact():
    data = request.json
    user_ip = get_user_ip(request)

    try:

        recaptcha = str(data['recaptcha'])

        first_name = str(data['first_name'])  # 0-50
        last_name = str(data['last_name'])  # 0-50
        email = str(data['email']).encode('ascii')  # 0-250
        message = str(data['message'])  # 20-500

        if (
            len(first_name) > 50 or
            len(last_name) > 50 or
            len(email) > 250 or
            len(message) < 20 or
            len(message) > 500
        ):
            raise ValueError

        verify_captcha(recaptcha, user_ip)

    # UnicodeEncodeError is completely unnecessary bc is a subclass of ValueError
    except (KeyError, ValueError, UnicodeEncodeError):
        return {'error': 'data'}, 400

    except (InvalidCaptcha, AttributeError):
        return {'error': 'captcha'}, 400

    now = int(time.time())

    try:
        contact_info = (
            user_ip,
            now + CONTACT_TIMEOUT,
            email
        )

        session_contact = session.get('contact')

        if session_contact is not None:
            if session_contact[1] > now:
                raise SendTimeout
        else:
            session['contact'] = contact_info

        if user_ip:
            if (doom_contact := get_doom_contact(user_ip)):
                if doom_contact[1] > now:
                    raise SendTimeout
            else:
                add_doom_contact(contact_info)

    except SendTimeout:
        return {'error': 'timeout'}, 400

    contact_hook(first_name, last_name, email, message)

    return {'success': True}
