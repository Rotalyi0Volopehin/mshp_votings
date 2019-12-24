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
        if (len(User.objects.filter(login=login)) > 0) or not ((0 < len(login) <= 32) and (0 < len(name) <= 32) and
                (0 < len(email) <= 32) and is_email_valid(email)):
            return False
        password_hash = password if password_as_hash else hash(password)
        user = User(first_name=name, email=email, login=login, password=password_hash, date_joined=datetime.datetime.today())
        user_data = UserData(user=user, activated=False, extra_info="")
        user.save()
        user_data.save()
        return True


def is_email_valid(email):
    if not isinstance(email, str):
        Exceptions.throw(Exceptions.argument_type)
    return re.match(email, r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")