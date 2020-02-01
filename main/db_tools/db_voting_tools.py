import datetime

from main.models import Voting
from main.models import VoteVariant
from main.models import VoteFact
from django.contrib.auth.models import User
from main.db_tools.db_user_tools import DB_UserTools
from exceptions import Exceptions


class DB_VotingTools:
    @staticmethod
    def try_create_voting(author, title, description, type_, show_votes_before_end, anonymous) -> (bool, str):
        if not (isinstance(author, User) and isinstance(title, str) and isinstance(description, str) and
                isinstance(type_, int) and isinstance(show_votes_before_end, bool) and isinstance(anonymous, bool)):
            Exceptions.throw(Exceptions.argument_type)
        if (type_ < 0) or (type_ > 2):
            Exceptions.throw(Exceptions.argument, "argument 'type_' must be integer from 0 to 2")
        if len(title) == 0:
            return False, "Здесь нет уязвимости!"
        ok, error = DB_UserTools.check_user_activation_required(author)
        if not ok:
            return False, error
        if DB_VotingTools.find_voting(author, title) != None:
            return False, "У вас уже существует голосование с таким названием!"
        voting = Voting(author=author, title=title, description=description, type=type_,
                show_votes_before_end=show_votes_before_end, anonymous=anonymous)
        voting.save()
        if type_ == 2: #Дискретное голосование всегда обладает только этими двумя вариантами голоса
            yes_var = VoteVariant(voting=voting, description="Да")
            no_var = VoteVariant(voting=voting, description="Нет")
            yes_var.save()
            no_var.save()
        user_data, _ = DB_UserTools.try_get_user_data(author)
        user_data.created_votings_count += 1
        user_data.save()
        return True, None

    @staticmethod
    def get_name_of_voting_type(type):
        if not isinstance(type, int):
            Exceptions.throw(Exceptions.argument_type)
        if (type < 0) or (type > 2):
            Exceptions.throw(Exceptions.argument, "argument 'type_' must be integer from 0 to 2")
        return "Множество из множества" if type == 0 else ("Один из множества" if type == 1 else "Дискретное")

    @staticmethod
    def clear_voting_list():
        Voting.objects.all().delete()

    @staticmethod
    def try_find_voting(author, title) -> (Voting, str):
        if not (isinstance(author, User) and isinstance(title, str)):
            Exceptions.throw(Exceptions.argument_type)
        voting = DB_VotingTools.find_voting(author, title)
        if voting is None:
            return None, "Голосование не найдено!"
        return voting, None

    @staticmethod
    def find_voting(author, title) -> Voting:
        voting = Voting.objects.filter(author=author, title=title)
        if len(voting) == 0:
            return None
        return voting[0]

    @staticmethod
    def try_find_voting_with_id(id) -> (Voting, str):
        voting = Voting.objects.filter(id=id)
        if len(voting) == 0:
            return None, "Голосование не найдено!"
        return voting[0], None

    @staticmethod
    def get_votings_of_user(user) -> [Voting]:
        if not isinstance(user, User):
            Exceptions.throw(Exceptions.argument_type)
        votings = Voting.objects.filter(author=user)
        return votings[:]

    @staticmethod
    def try_add_vote_variant(author, voting, description) -> (bool, str):
        if not (isinstance(author, User), isinstance(voting, Voting) and isinstance(description, str)):
            Exceptions.throw(Exceptions.argument_type)
        if author != voting.author:
            return False, "Вы не являетесь автором указанного голосования!"
        if voting.started:
            return False, "Нельзя изменять {} голосование!".format("законченное" if voting.completed else "начатое")
        if voting.type == 2:
            return False, "Нельзя изменять варианты голоса дискретного голосования!"
        neighbour_variants = VoteVariant.objects.filter(voting=voting)
        for neighbour_variant in neighbour_variants:
            if neighbour_variant.description == description:
                return False, "В этом голосование уже есть вариант голоса с указанным описанием!"
        if (len(description) == 0) or (len(description) > 4096):
            return False, "Здесь нет уязвимости!"
        variant = VoteVariant(voting=voting, description=description)
        variant.save()
        return True, None

    @staticmethod
    def clear_vote_variant_list():
        VoteVariant.objects.all().delete()

    @staticmethod
    def try_start_voting(author, voting) -> (bool, str):
        if not (isinstance(author, User) and isinstance(voting, Voting)):
            Exceptions.throw(Exceptions.argument_type)
        if author != voting.author:
            return False, "Вы не являетесь автором указанного голосования!"
        if voting.completed:
            return False, "Указанное голосование уже завершено!"
        if voting.started:
            return False, "Указанное голосование уже начато!"
        vote_variant_count = len(VoteVariant.objects.filter(voting=voting))
        if vote_variant_count == 0:
            return False, "Голосование не может не иметь вариантов голоса!"
        voting.started = True
        voting.date_started = datetime.datetime.now()
        voting.save()
        return True, None

    @staticmethod
    def try_stop_voting(author, voting) -> (bool, str):
        if not (isinstance(author, User) and isinstance(voting, Voting)):
            Exceptions.throw(Exceptions.argument_type)
        if author != voting.author:
            return False, "Вы не являетесь автором указанного голосования!"
        if not voting.started:
            return False, "Указанное голосование ещё не начато!"
        if voting.completed:
            return False, "Указанное голосование уже завершено!"
        voting.completed = True
        voting.date_stopped = datetime.datetime.now()
        voting.save()
        return True, None

    @staticmethod
    def get_voting_info(voting, user=None) -> [str]:
        if not (isinstance(voting, Voting) and (user is None or isinstance(user, User))):
            Exceptions.throw(Exceptions.argument_type)
        info = ["Информация о голосовании:"]
        info.append("Логин автора : " + ("$_del" if voting.author is None else voting.author.username))
        info.append("Название : " + voting.title)
        info.append("Дата и время создания : " + str(voting.date_created))
        info.append("Тип : " + DB_VotingTools.get_name_of_voting_type(voting.type))
        info.append("Статус : ")
        if voting.completed:
            info[-1] += "завершено"
            info.append("Дата и время завершения : " + str(voting.date_stopped))
        elif voting.started:
            info[-1] += "идёт"
        else:
            info[-1] += "ещё не начато"
        if voting.started:
            info.append("Дата и время начала : " + str(voting.date_started))
        vote_variants = VoteVariant.objects.filter(voting=voting)
        if (user != None) and voting.started:
            vote_fact = VoteFact.objects.filter(user=user, voting=voting)
            vote_fact_count = len(vote_fact)
            if vote_fact_count > 1:
                return ["Вы проголосовали {} раз в этом голосовании! Вы хакер?".format(vote_fact_count)]
            elif vote_fact_count == 1:
                vote_fact = vote_fact[0]
                info.append("Вы принимали участие в этом голосовании")
        info.append("Открытая статистика голосов до окончания голосования : " +
                    ("вкл." if voting.show_votes_before_end else "выкл."))
        info.append("Анонимность голосования : " + ("вкл." if voting.anonymous else "выкл."))
        if len(vote_variants) == 0:
            info.append("Вариантов голоса нет")
        else:
            info.append("Варианты голоса:")
            show_votes = voting.completed or (voting.started and voting.show_votes_before_end)
            show_answers = (user != None) and voting.started and (vote_fact_count == 1) and not voting.anonymous
            if show_answers:
                bin_answer = vote_fact.answer
            for vote_variant in vote_variants:
                info.append("- " + vote_variant.description)
                if show_votes:
                    info.append(str(vote_variant.vote_fact_count) + " голос(а/ов)")
                if show_answers:
                    if bin_answer & 1:
                        info.append("Ваш голос")
                    bin_answer >>= 1
        return info

    @staticmethod
    def try_vote(user, voting, answers) -> (bool, str):
        if not (isinstance(user, User) and isinstance(voting, Voting) and isinstance(answers, list)):
            Exceptions.throw(Exceptions.argument_type)
        yes_var = bin_answer = 0
        for answer in answers[::-1]:
            if not isinstance(answer, bool):
                Exceptions.throw(Exceptions.argument_type)
            bin_answer = (bin_answer << 1) | answer
            if answer:
                yes_var += 1
        ok, error = DB_UserTools.check_user_activation_required(user)
        if not ok:
            return False, error
        if voting.completed:
            return False, "Голосование уже завершено!"
        if not voting.started:
            return False, "Голосование ещё не начато!"
        variants = VoteVariant.objects.filter(voting=voting)
        if len(variants) != len(answers):
            return False, "Длина голоса не совпадает с количеством вариантов голоса!"
        if voting.type != 0:
            if yes_var != 1:
                return False, "Тип голосования '{}' подразумевает голос ровно за 1 вариант!".format(
                        DB_VotingTools.get_name_of_voting_type(voting.type))
        if len(VoteFact.objects.filter(user=user, voting=voting)) > 0:
            return False, "Вы уже проголосовали!"
        # TODO - если 2 пользователя проголосуют одновременно, vote_fact_count увеличится лишь на 1 голос из-за наложения; надо починить
        for i in range(len(answers)):
            if answers[i]:
                variants[i].vote_fact_count += 1
                variants[i].save()
        if voting.anonymous:
            bin_answer = 0
        vote_fact = VoteFact(user=user, voting=voting, answer=bin_answer)
        vote_fact.save()
        user_data, _ = DB_UserTools.try_get_user_data(user)
        user_data.vote_count += 1
        user_data.save()
        return True, None

    @staticmethod
    def clear_vote_fact_list():
        VoteFact.objects.all().delete()