import datetime

from main.db_tools.db_voting_tools import DB_VotingTools
from main.models import Voting
from main.models import VotingAbuse
from django.contrib.auth.models import User
from main.db_tools.db_user_tools import DB_UserTools
from exceptions import Exceptions


class DB_AbuseTools:
    @staticmethod
    def try_create_abuse(author, title, description, voting) -> (bool, str):
        if not(isinstance(author, User) and isinstance(title, str) and isinstance(description, str) and isinstance(voting, Voting)):
            Exceptions.throw(Exceptions.argument_type)
        if len(title) == 0:
            return False, "Здесь нет уязвимости!"
        #ok, error = DB_UserTools.check_user_activation_required(author)
        ok = True
        if not ok:
            return False, "Пользователь не активировал почту"
        abuse = VotingAbuse(abuser=author, voting=voting, description=description)
        abuse.save()
        return True, None