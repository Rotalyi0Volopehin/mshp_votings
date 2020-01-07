import re
import datetime

from django.contrib.auth.models import User
from main.models import UserData
from exceptions import Exceptions


class DB_UserTools:
    @staticmethod
    def try_register_user(login, password, name, email) -> (bool, str):
        if not (isinstance(login, str) and isinstance(password, str) and isinstance(name, str) and isinstance(email, str)):
            Exceptions.throw(Exceptions.argument_type)
        if (len(User.objects.filter(username=login)) > 0) or not ((0 < len(login) <= 32) and (0 < len(name) <= 32) and
                (0 < len(email) <= 32)):
                return (False, "Пользователь с данным логином уже существует!")
        if not is_email_valid(email):
            return (False, "E-mail некорректен!")
        user = User(first_name=name, email=email, username=login, date_joined=datetime.datetime.today())
        user.set_password(password)
        user.save()
        user_data = UserData()
        user_data.user = user
        user_data.activated = True #must be False
        user_data.extra_info = ""
        user_data.save()
        return (True, None)

    @staticmethod
    def clear_user_list():
        User.objects.all().delete()
        UserData.objects.all().delete()


__email_re = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


def is_email_valid(email):
    return __email_re.match(email)