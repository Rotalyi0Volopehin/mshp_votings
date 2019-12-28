import re
import datetime

from django.contrib.auth.models import User
from main.models import UserData
from exceptions import Exceptions


class DB_UserTools:
    @staticmethod
    def try_register_user(login, password, name, email, password_as_hash=False) -> bool:
        if not (isinstance(login, str) and isinstance(password, str) and isinstance(name, str) and\
                isinstance(email, str) and isinstance(password_as_hash, bool)):
            Exceptions.throw(Exceptions.argument_type)
        if (len(User.objects.filter(username=login)) > 0) or not ((0 < len(login) <= 32) and (0 < len(name) <= 32) and
                (0 < len(email) <= 32)):
                return False
        if not is_email_valid(email):
            return False
        password_hash = password if password_as_hash else calc_password_hash(password)
        user = User(first_name=name, email=email, username=login, password=password_hash, date_joined=datetime.datetime.today())
        user.save()
        user_data = UserData()
        user_data.user = user
        user_data.activated = False
        user_data.extra_info = ""
        user_data.save()
        return True

    @staticmethod
    def clear_user_list():
        User.objects.all().delete()
        UserData.objects.all().delete()


__email_re = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


def is_email_valid(email):
    return __email_re.match(email)


def calc_password_hash(password):
    return password #временно
    if not isinstance(password, str):
        Exceptions.throw(Exceptions.argument_type)
    mul = 1
    for char in password:
        mul *= hash(char)
    mul = str(mul)
    hcode = ""
    for i in range(len(mul)):
        if (i & 1) == 1:
            hcode += chr(int(mul[i - 1] + mul[i + 1]))
    if (len(mul) & 1) == 1:
        hcode += mul[-1]
    return hcode