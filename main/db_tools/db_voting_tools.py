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
        author_data = UserData.objects.filter(user=author)
        if (len(author_data) != 1) or not author_data[0].activated:
            return False
        if len(title) == 0:
            return False
        voting = Voting(author=author, title=title, description=description, type=type_,
                show_votes_before_end=show_votes_before_end, anonymous=anonymous)
        voting.started = voting.completed = False
        voting.save()
        return True