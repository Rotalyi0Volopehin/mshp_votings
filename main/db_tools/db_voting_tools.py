import datetime

from main.models import Voting
from main.models import VoteVariant
from django.contrib.auth.models import User
from main.models import UserData
from exceptions import Exceptions


class DB_VotingTools:
    @staticmethod
    def try_create_voting(author, title, description, type_, show_votes_before_end, anonymous):
        if not (isinstance(author, User) and isinstance(title, str) and isinstance(description, str) and
                isinstance(type_, int) and isinstance(show_votes_before_end, bool) and isinstance(anonymous, bool)):
            Exceptions.throw(Exceptions.argument_type)
        if (type_ < 0) or (type_ > 2):
            Exceptions.throw(Exceptions.argument, "argument \"type_\" must be integer from 0 to 2")
        if len(title) == 0:
            return False
        author_data = UserData.objects.filter(user=author)
        if (len(author_data) != 1) or not author_data[0].activated:
            return False
        if len(Voting.objects.filter(author=author, title=title)) > 0:
            return False
        voting = Voting(author=author, title=title, description=description, type=type_,
                show_votes_before_end=show_votes_before_end, anonymous=anonymous)
        voting.started = voting.completed = False
        voting.save()
        voting.date_created = datetime.datetime.today()
        return True

    def try_add_vote_variant(self, voting, description):
        if not (isinstance(voting, Voting) and isinstance(description, str)):
            Exceptions.throw(Exceptions.argument_type)
        if len(Voting.objects.filter(author=voting.author, title=voting.title)) > 0:
            Exceptions.throw(Exceptions.argument, "voting must be in the DB")
        if (len(description) == 0) or (len(description) > 4096):
            return False
        variant = VoteVariant(voting, description)
        variant.save()
        return True