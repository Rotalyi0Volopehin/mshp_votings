from main.models import Voting
from main.db_tools.db_user_tools import DB_UserTools
from exceptions import Exceptions


class VotingSearchFilter:
    def __init__(self, exclude_not_started=False, exclude_not_completed=False, exclude_started=False, exclude_completed=False):
        if not (isinstance(exclude_not_started, bool) and isinstance(exclude_not_completed, bool) and
                isinstance(exclude_started, bool) and isinstance(exclude_completed, bool)):
            Exceptions.throw(Exceptions.argument_type)
        self.exclude_not_started = exclude_not_started
        self.exclude_not_completed = exclude_not_completed
        self.exclude_started = exclude_started
        self.exclude_completed = exclude_completed

    def does_voting_match(self, voting) -> bool:
        if not isinstance(voting, Voting):
            Exceptions.throw(Exceptions.argument_type)
        if self.exclude_not_started and not voting.started:
            return False
        if self.exclude_not_completed and not voting.completed:
            return False
        if self.exclude_started and voting.started:
            return False
        if self.exclude_completed and voting.completed:
            return False
        return True

    def filter(self, votings):
        if self.exclude_not_started:
            votings = votings.filter(started=True)
        if self.exclude_not_completed:
            votings = votings.filter(completed=True)
        if self.exclude_started:
            votings = votings.filter(started=False)
            if self.exclude_completed:
                votings = votings.filter(completed=False)
        return votings


class DB_SearchTools:
    @staticmethod
    def search_for_voting(voting_title=None, author_login=None, filter=VotingSearchFilter()) -> [Voting]:
        if not ((isinstance(voting_title, str) or (voting_title is None)) and
                ((isinstance(author_login, str) or (author_login is None))) and isinstance(filter, VotingSearchFilter)):
            Exceptions.throw(Exceptions.argument_type)
        votings = Voting.objects.all()
        if voting_title != None:
            votings = votings.filter(title=voting_title)
        if author_login != None:
            author = DB_UserTools.try_find_user(author_login)
            if author is None:
                return []
            votings = votings.filter(author=author)
        votings = filter.filter(votings)
        return votings[:]