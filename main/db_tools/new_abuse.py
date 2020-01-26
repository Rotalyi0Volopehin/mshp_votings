import datetime

from main.db_tools.db_voting_tools import DB_VotingTools
from main.models import Voting
from main.models import VotingAbuse
from django.contrib.auth.models import User
from main.db_tools.db_user_tools import DB_UserTools
from exceptions import Exceptions


class DB_AbuseTools:
    @staticmethod
    def try_create_abuse(author, title, description) -> (bool, str):
        if not (isinstance(author, User) and isinstance(title, str) and isinstance(description, str)):
            Exceptions.throw(Exceptions.argument_type)
        if len(title) == 0:
            return False, "Здесь нет уязвимости!"
        if DB_VotingTools.find_voting(author, title) != None:
            return False, "Голосование не найдено!"
        ok, error = DB_UserTools.check_user_activation_required(author)
        if not ok:
            return False, error
        abuse = VotingAbuse(abuser=author, voting=title, description=description)
        abuse.save()
        return True, None