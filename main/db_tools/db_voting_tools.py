import datetime

from main.models import Voting
from main.models import VoteVariant
from django.contrib.auth.models import User
from main.models import UserData
from exceptions import Exceptions


class DB_VotingTools:
    @staticmethod
    def try_create_voting(author, title, description, type_, show_votes_before_end, anonymous) -> (bool, str):
        if not (isinstance(author, User) and isinstance(title, str) and isinstance(description, str) and
                isinstance(type_, int) and isinstance(show_votes_before_end, bool) and isinstance(anonymous, bool)):
            Exceptions.throw(Exceptions.argument_type)
        if (type_ < 0) or (type_ > 2):
            Exceptions.throw(Exceptions.argument, "argument \"type_\" must be integer from 0 to 2")
        if len(title) == 0:
            return False, "Здесь нет уязвимости!"
        author_data = UserData.objects.filter(user=author)
        if len(author_data) != 1:
            return False, "Некорректная конфигурация пользовательских данных!"
        if not author_data[0].activated:
            return False, "Пользователь не активирован!"
        if DB_VotingTools.find_voting(author, title) != None:
            return False, "У вас уже существует голосование с таким названием!"
        voting = Voting(author=author, title=title, description=description, type=type_)
        voting.show_votes_before_end = show_votes_before_end
        voting.anonymous = anonymous
        voting.started = voting.completed = False
        # TODO - add next feature : voting.date_created = datetime.datetime.today()
        voting.save()
        return True, None

    @staticmethod
    def clear_voting_list():
        Voting.objects.all().delete()

    @staticmethod
    def find_voting(author, title) -> Voting:
        such_votings = Voting.objects.filter(author=author)
        for voting in such_votings:
            if voting.title == title:
                return voting
        return None

    @staticmethod
    def try_add_vote_variant(author, voting_title, description) -> (bool, str):
        if not (isinstance(voting_title, str) and isinstance(description, str)):
            Exceptions.throw(Exceptions.argument_type)
        voting = DB_VotingTools.find_voting(author, voting_title)
        if voting is None:
            return False, "У вас нет голосования с указанным названием!"
        if voting.started:
            return False, "Нельзя изменять начатое голосование!"
        if (len(description) == 0) or (len(description) > 4096):
            return False, "Здесь нет уязвимости!"
        variant = VoteVariant(voting, description)
        variant.save()
        return True, None