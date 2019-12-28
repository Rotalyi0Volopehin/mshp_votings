import datetime

from main.db_tools.db_user_tools import DB_UserTools
from main.db_tools.db_voting_tools import DB_VotingTools
from main.db_tools.db_user_tools import calc_password_hash
from django.contrib.auth import views as auth_views
from django.shortcuts import render
import main.forms
from django.contrib.auth.decorators import login_required



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


def registration_page(request): #временно
    context = {}
    ok = False
    if request.method == "POST":
        form = main.forms.RegistrationForm(request.POST)
        context["form"] = form
        if form.is_valid():
            ok = DB_UserTools.try_register_user(form.data["login"], form.data["password1"], form.data["name"], form.data["email"])
    else:
        context["form"] = main.forms.RegistrationForm()
        ok = True
    context["ok"] = ok
    return render(request, 'registration/registration.html', context)


__login_view = auth_views.LoginView.as_view(extra_context={'menu': get_menu_context(), 'pagename': 'Авторизация'})


def login_cloak(request):
    if (request.method == "POST") and request.POST and ("password" in request.POST):
        password = request.POST["password"]
        if 0 < len(password) <= 32:
            request.POST = request.POST.copy()
            #request.POST["password"] = calc_password_hash(password)
    return __login_view(request)


@login_required
def new_voting_page(request):
    context = {}
    ok = False
    if (request.method == "POST") and request.POST:
        form = main.forms.NewVotingForm(request.POST)
        context["form"] = form
        if form.is_valid():
            author = request.user
            data = form.data
            ok = DB_VotingTools.try_create_voting(author, data["title"], data["discription"], data["type"],
                    data["show_votes_before_end"], data["anonymous"])
    else:
        context["form"] = main.forms.NewVotingForm()
        ok = True
    context["ok"] = ok
    return render(request, "pages/new_voting.html", context)


def clear_user_list_page(request): #временно
    DB_UserTools.clear_user_list()