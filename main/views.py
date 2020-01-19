import datetime
import main.forms

from main.db_tools.db_user_tools import DB_UserTools
from main.db_tools.db_voting_tools import DB_VotingTools
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser


def get_menu_context():
    return [
        {'url': '/', 'name': 'Главная'},
        {'url': '/time/', 'name': 'Текущее время'},
    ]


def index_page(request):
    context = {
        'pagename': 'Главная',
        'author': 'Andrew',
        'pages': 4,
        'menu': get_menu_context()
    }
    return render(request, 'pages/index.html', context)


def time_page(request):
    context = {
        'pagename': 'Текущее время',
        'time': datetime.datetime.now().time(),
        'menu': get_menu_context()
    }
    return render(request, 'pages/time.html', context)


def view_func_template(request, html_path, form_class, body):
    context = {}
    success = ok = False
    error = None
    if request.method == "POST":
        form = form_class(request.POST)
        context["form"] = form
        if form.is_valid():
            ok, error, success = body(form, context)
        else:
            error = "Здесь нет уязвимости!"
    else:
        context["form"] = form_class()
        ok = True
    context["ok"] = ok
    context["error"] = error
    context["success"] = success
    return render(request, html_path, context)


def __demo_for_view_func_template(request):
    def body(form, context) -> (bool, str, bool):
        success = ok = False
        error = None
        # body code
        return ok, error, success
    return view_func_template(request, '~html path~', '~form class~', body)


def registration_page(request): #временно
    def body(form, context) -> (bool, str, bool):
        success = ok = False
        password1 = form.data["password1"]
        if password1 == form.data["password2"]:
            ok, error = DB_UserTools.try_register_user(form.data["login"], password1, form.data["name"], form.data["email"])
            success = ok
        else:
            error = "Указанные пароли не совпадают!"
        return ok, error, success
    return view_func_template(request, "registration/registration.html", main.forms.RegistrationForm, body)


def clear_all_data_page(request): #Developer's tool
    DB_VotingTools.clear_vote_fact_list()
    DB_VotingTools.clear_vote_variant_list()
    DB_VotingTools.clear_voting_list()
    DB_UserTools.clear_user_list()
    return render(request, 'pages/cad.html')


@login_required
def new_voting_page(request): #временно
    def body(form, context) -> (bool, str, bool):
        author = request.user
        title = form.data["title"]
        description = form.data["description"]
        type_ = int(form.data["type"]) - 1
        show_votes_before_end = form.data.get("show_votes_before_end", 'off') == 'on'
        anonymous = form.data.get("anonymous", 'off') == 'on'
        ok, error = DB_VotingTools.try_create_voting(author, title, description, type_, show_votes_before_end, anonymous)
        success = ok
        return ok, error, success
    return view_func_template(request, "pages/voting_management/new_voting.html", main.forms.NewVotingForm, body)


@login_required
def add_vote_variant_page(request): #временно
    def body(form, context) -> (bool, str, bool):
        author = request.user
        voting_title = form.data["voting_title"]
        description = form.data["description"]
        ok, error = DB_VotingTools.try_add_vote_variant(author, voting_title, description)
        success = ok
        return ok, error, success
    return view_func_template(request, "pages/voting_management/add_vote_variant.html", main.forms.AddVoteVariantForm, body)


@login_required
def run_voting_page(request): #временно
    def body(form, context) -> (bool, str, bool):
        success = False
        author = request.user
        voting_title = form.data["voting_title"]
        start_not_stop = int(form.data["action"]) == 1
        ok, error = DB_VotingTools.try_start_voting(author, voting_title) if start_not_stop else\
                DB_VotingTools.try_stop_voting(author, voting_title)
        if ok:
            success = True
            context["success_message"] = "Голосование успешно " + ("начато" if start_not_stop else "завершено")
        return ok, error, success
    return view_func_template(request, "pages/voting_management/run_voting.html", main.forms.RunVotingForm, body)


def voting_info_page(request): #временно
    def body(form, context) -> (bool, str, bool):
        success = ok = False
        author_login = form.data["author_login"]
        voting_title = form.data["voting_title"]
        voting, error = DB_VotingTools.try_find_voting(author_login, voting_title)
        if voting != None:
            ok = success = True
            user = None if isinstance(request.user, AnonymousUser) else request.user
            context["info"] = DB_VotingTools.get_voting_info(voting, user)
        return ok, error, success
    return view_func_template(request, "pages/voting_management/voting_info.html", main.forms.SearchVotingForm, body)


@login_required
def vote_page(request): #временно
    def body(form, context) -> (bool, str, bool):
        success = ok = False
        author_login = form.data["author_login"]
        voting_title = form.data["voting_title"]
        voting, error = DB_VotingTools.try_find_voting(author_login, voting_title)
        if voting != None:
            answers = []
            text_answer = form.data["answer"]
            for digit in text_answer:
                if digit == '0':
                    answers.append(False)
                elif digit == '1':
                    answers.append(True)
                else:
                    error = "Голос не должен содержать других символов, кроме '0' или '1'!"
                    break
            if error is None:
                ok, error = DB_VotingTools.try_vote(request.user, voting, answers)
            success = ok
        return ok, error, success
    return view_func_template(request, "pages/vote.html", main.forms.VoteForm, body)