from main.models import Voting
from main.db_tools.db_user_tools import DB_UserTools
from exceptions import Exceptions


class SearchFilterOption:
    def __init__(self, type_): #private
        if not isinstance(type_, int):
            Exceptions.throw(Exceptions.argument_type)
        if (type_ < -1) or (type_ > 1):
            Exceptions.throw(Exceptions.argument, "argument 'type_' must be contained by segment [-1; 1]")
        self.__type = type_

    @property
    def type(self):
        return self.__type

    @staticmethod
    def empty():
        return SearchFilterOption(0)

    @staticmethod
    def exclude():
        return SearchFilterOption(1)

    @staticmethod
    def exclude_all_other():
        return SearchFilterOption(-1)


class VotingSearchFilter:
    __default_option = SearchFilterOption.empty()

    def __init__(self, started_option=__default_option, completed_option=__default_option,
            show_votes_before_end_option=__default_option, anonymous_option=__default_option):
        if not (isinstance(anonymous_option, SearchFilterOption) and isinstance(completed_option, SearchFilterOption) and
                isinstance(show_votes_before_end_option, SearchFilterOption) and isinstance(started_option, SearchFilterOption)):
            Exceptions.throw(Exceptions.argument_type)
        self.started_option = started_option
        self.completed_option = completed_option
        self.show_votes_before_end_option = show_votes_before_end_option
        self.anonymous_option = anonymous_option

    def filter(self, votings):
        if self.started_option.type != 0:
            votings = votings.filter(started=(self.started_option.type == -1))
        if self.completed_option.type != 0:
            votings = votings.filter(completed=(self.completed_option.type == -1))
        if self.show_votes_before_end_option.type != 0:
            votings = votings.filter(show_votes_before_end=(self.show_votes_before_end_option.type == -1))
        if self.anonymous_option.type != 0:
            votings = votings.filter(anonymous=(self.anonymous_option.type == -1))
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
            author, _ = DB_UserTools.try_find_user(author_login)
            if author is None:
                return []
            votings = votings.filter(author=author)
        votings = filter.filter(votings)
        return votings[:]