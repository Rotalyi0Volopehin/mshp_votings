import re
import datetime

from django.contrib.auth.models import User
from main.models import UserData
from exceptions import Exceptions
# for email confirmation vvv
from main.db_tools.tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage


class DB_UserTools:
    @staticmethod
    def try_register_user(login, password, name, email, request) -> (bool, str):
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
        user_data = UserData(user=user)
        user_data.activated = False
        user_data.save()
        DB_UserTools.__ask_for_email_confirmation(user, request)
        return True, None

    @staticmethod
    def __ask_for_email_confirmation(user, request):
        subject = "Активация аккаунта онлайн голосований"
        current_site = get_current_site(request)
        token = account_activation_token.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_link = "{0}/activate/{1}/{2}/".format(current_site, uid, token)
        message = "Activation link:\n" + activation_link
        email = EmailMessage(subject, message, to=[user.email])
        email.send()

    @staticmethod
    def try_activate_user(user) -> bool:
        if not isinstance(user, User):
            Exceptions.throw(Exceptions.argument_type)
        user_data = UserData.objects.filter(user=user)
        if len(user_data) == 0:
            return False
        user_data = user_data[0]
        if not user_data.activated:
            user_data.activated = True
            user_data.save()
        return True

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