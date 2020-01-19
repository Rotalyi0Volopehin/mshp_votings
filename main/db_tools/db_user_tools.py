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
        if not ((0 < len(login) <= 64) and (0 < len(name) <= 64) and (0 < len(email) <= 64) and (0 < len(password) <= 64)):
            return False, "Здесь нет уязвимости!"
        if len(User.objects.filter(username=login)) > 0:
            return False, "Пользователь с данным логином уже существует!"
        if not is_email_valid(email):
            return False, "E-mail некорректен!"
        if len(User.objects.filter(email=email)) > 0:
            return False, "Пользователь с указанным E-mail уже существует!"
        user = User(first_name=name, email=email, username=login, date_joined=datetime.datetime.today())
        user.set_password(password)
        user.save()
        user_data = UserData()
        user_data.user = user
        user_data.activated = True #must be False
        user_data.extra_info = ""
        user_data.save()
        return True, None

    @staticmethod
    def try_find_user(login) -> (User, str):
        if not isinstance(login, str):
            Exceptions.throw(Exceptions.argument_type)
        user = DB_UserTools.find_user(login)
        if user is None:
            return None, "Пользователь не найден!"
        return user, None

    @staticmethod
    def find_user(login) -> User:
        user = User.objects.filter(username=login)
        if len(user) == 0:
            return None
        return user[0]

    @staticmethod
    def check_user_activation_required(user) -> (bool, str):
        if not isinstance(user, User):
            Exceptions.throw(Exceptions.argument_type)
        user_data = UserData.objects.filter(user=user)
        if len(user_data) != 1:
            return False, "Некорректная конфигурация пользовательских данных!"
        if not user_data[0].activated:
            return False, "Пользователь не активирован!"
        return True, None

    @staticmethod
    def clear_user_list():
        UserData.objects.all().delete()
        User.objects.all().delete()


__email_re = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


def is_email_valid(email):
    return __email_re.match(email)