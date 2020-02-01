import main.forms
import main.models
import main.db_tools.db_search_tools

from main.db_tools.db_user_tools import DB_UserTools
from main.db_tools.db_voting_tools import DB_VotingTools
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import login, logout


def get_menu_context():
    return [
        {'url': '/', 'name': 'Главная'},
        {'url': '/search_v/', 'name': 'Поиск голосований'}
    ]


def index_page(request):
    context = {
        'pagename': 'Главная',
        'author': 'Andrew',
        'pages': 4,
        'menu': get_menu_context()
    }
    return render(request, 'pages/index.html', context)


def view_func_template(request, html_path, form_class, post_handler, get_handler=None, context=None):
    if context is None:
        context = {}
    context["menu"] = get_menu_context()
    success = ok = False
    error = None
    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            ok, error, success = post_handler(form=form, context=context)
        else:
            error = "Неверный формат отосланных данных!"
    else:
        if get_handler is None:
            form = form_class()
            ok = True
        else:
            ok, error, success, form = get_handler(context=context)
    context["form"] = form
    context["ok"] = ok
    context["error"] = error
    context["success"] = success
    return render(request, html_path, context)


def __demo_of_view_func_template(request):
    def post_handler(form, context) -> (bool, str, bool):
        success = ok = False
        error = None
        # post_handler code
        return ok, error, success
    return view_func_template(request, '~html path~', '~form class~', post_handler)


def registration_page(request):
    def post_handler(form, context) -> (bool, str, bool):
        success = ok = False
        password1 = form.data["password1"]
        if password1 == form.data["password2"]:
            login_ = form.data["login"]
            ok, error = DB_UserTools.try_register_user(login_, password1, form.data["name"], form.data["email"], request)
            success = ok
        else:
            error = "Указанные пароли не совпадают!"
        return ok, error, success
    return view_func_template(request, "registration/registration.html", main.forms.RegistrationForm, post_handler)


def clear_all_data_page(request): #Developer's tool
    DB_VotingTools.clear_vote_fact_list()
    DB_VotingTools.clear_vote_variant_list()
    DB_VotingTools.clear_voting_list()
    DB_UserTools.clear_user_list()
    return render(request, 'pages/cad.html')


@login_required
def new_voting_page(request):
    def post_handler(form, context) -> (bool, str, bool):
        context["pagename"] = "Новое голосование"
        author = request.user
        title = form.data["title"]
        description = form.data["description"]
        type_ = int(form.data["type"])
        show_votes_before_end = form.data.get("show_votes_before_end", 'off') == 'on'
        anonymous = form.data.get("anonymous", 'off') == 'on'
        ok, error = DB_VotingTools.try_create_voting(author, title, description, type_, show_votes_before_end, anonymous)
        success = ok
        return ok, error, success
    return view_func_template(request, "pages/voting_management/new_voting.html", main.forms.NewVotingForm, post_handler)


@login_required
def vote_page(request, id):
    voting, error = DB_VotingTools.try_find_voting_with_id(id)
    vars = []
    if error is None:
        variants = main.models.VoteVariant.objects.filter(voting=voting)[:]
        for i in range(len(variants)):
            vars.append((i, variants[i].description))
    if request.method == "GET":
        form = main.forms.VoteForm()
        context = { "menu": get_menu_context(), "pagename": "Голосование", "form": form }
        form.fields["answer"].widget.attrs["value"] = "0" * len(vars)
        context["vars"] = vars
        context["error"] = error
        context["ok"] = error is None
        return render(request, "pages/vote.html", context)
    def body(form, context) -> (bool, str, bool):
        form.fields["answer"].widget.attrs["value"] = "0" * len(vars)
        context["menu"] = get_menu_context()
        context["pagename"] = "Голосование"
        context["vars"] = vars
        success = ok = False
        voting, error = DB_VotingTools.try_find_voting_with_id(id)
        if error is None:
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


def voting_search_page(request):
    page_size = 16
    def body(form, context) -> (bool, str, bool):
        context["page_size"] = page_size
        offset = form.data["offset"]
        offset = int(offset) if str.isdigit(offset) else 0
        author_login = form.data["author_login"]
        voting_title = form.data["voting_title"]
        if len(author_login) == 0:
            author_login = None
        if len(voting_title) == 0:
            voting_title = None
        started_option = int(form.data["started_option"])
        started_option = main.db_tools.db_search_tools.SearchFilterOption(started_option)
        completed_option = int(form.data["completed_option"])
        completed_option = main.db_tools.db_search_tools.SearchFilterOption(completed_option)
        show_votes_before_end_option = int(form.data["show_votes_before_end_option"])
        show_votes_before_end_option = main.db_tools.db_search_tools.SearchFilterOption(show_votes_before_end_option)
        anonymous_option = int(form.data["anonymous_option"])
        anonymous_option = main.db_tools.db_search_tools.SearchFilterOption(anonymous_option)
        filter = main.db_tools.db_search_tools.VotingSearchFilter(started_option, completed_option, show_votes_before_end_option, anonymous_option)
        votings, end = main.db_tools.db_search_tools.DB_SearchTools.search_for_voting(voting_title, author_login, filter, offset, page_size)
        context["votings"] = votings
        context["prev_page"] = offset > 0
        context["next_page"] = not end
        return True, None, True
    return view_func_template(request, "pages/voting_search.html", main.forms.SearchVotingForm, body)


def voting_info_page(request, id):
    context = {"menu": get_menu_context(), "pagename": "Информация о голосовании"}
    ok = False
    voting, error = DB_VotingTools.try_find_voting_with_id(id)
    if error is None:
        user = None if isinstance(request.user, AnonymousUser) else request.user
        context["info"] = DB_VotingTools.get_voting_info(voting, user)
        ok = True
        can_vote = context["can_vote"] = (user != None) and DB_UserTools.can_vote(user, voting)
        if can_vote:
            context["vote_ref"] = "/vote/{}/".format(voting.id)
        context["voting"] = voting
        context["voting_type"] = DB_VotingTools.voting_type_names[voting.type]
    context["ok"] = ok
    context["error"] = error
    return render(request, "pages/voting_info.html", context)


@login_required
def my_votings_page(request):
    votings = DB_VotingTools.get_votings_of_user(request.user)
    context = {"menu": get_menu_context(), "pagename": "Мои голосования", "votings": votings}
    context["type_names"] = DB_VotingTools.voting_type_names
    return render(request, "pages/voting_management/my_votings.html", context)


def profile_page(request, id):
    context = {}
    def body(form=None, context=None):
        ok = success = False
        user, error = DB_UserTools.try_find_user_with_id(id)
        if error is None:
            user_data, error = DB_UserTools.try_get_user_data(user)
            if error is None:
                self = context['self'] = not isinstance(request.user, AnonymousUser) and (user.id == request.user.id)
                context['pagename'] = "Мой профиль" if self else "Профиль"
                if self and (form != None):
                    ok, error, success = post_handler(form, context, user, user_data)
                context['login'] = user.username
                context['name'] = user.first_name
                context['email'] = user.email
                context['regdate'] = user.date_joined
                context['createdpolls'] = user_data.created_votings_count
                context['votedpolls'] = user_data.vote_count
                context['activated'] = user_data.activated
                context['about'] = user_data.extra_info
        else:
            context["pagename"] = "Профиль"
        result = [ok, error, success]
        if form is None:
            result.append(None)
        return result
    def post_handler(form, context, user, user_data):
        success = ferr = False
        error = None
        action = form.data["action"]
        if action == "save-chan":
            name = form.data["name"]
            if 0 < len(name) <= 64:
                about = form.data["about"]
                user.first_name = name
                user.save()
                user_data.extra_info = about
                user_data.save()
                success = True
            else:
                ferr = True
        elif action == "save-pass":
            password = form.data["password"]
            if user.check_password(password):
                new_password = form.data["new_password"]
                if 0 < len(new_password) <= 64:
                    user.set_password(new_password)
                    user.save()
                    success = True
                else:
                    error = "Длина пароля должна быть больше 1, но меньше 65 символов!"
            else:
                error = "Текущий пароль не совпадает с указанным!"
        elif action == "del":
            logout(request)
            user.delete()
            context["del"] = success = True
        else:
            ferr = True
        if ferr:
            error = "Неверный формат отосланных данных!"
        return success, error, success
    result = view_func_template(request, "pages/profile.html", main.forms.ProfileForm, body, get_handler=body, context=context)
    return redirect("/") if "del" in context else result


@login_required
def my_profile_page(request):
    return profile_page(request, request.user.id)


@login_required
def manage_voting_page(request, id):
    def body(form=None, context=None) -> (bool, str, bool):
        context["pagename"] = "Работа над голосованием"
        get_method = form is None
        if get_method:
            form = main.forms.ManageVotingForm()
        ok = success = False
        voting, error = DB_VotingTools.try_find_voting_with_id(id)
        if error is None:
            if voting.author == request.user:
                addv_lock = voting.started or (voting.type == 2)
                if not get_method:
                    ok, error, addv_lock = post_handler(form, context, voting, addv_lock)
                    success = ok
                if error is None:
                    if addv_lock:
                        form.fields["description"].widget.attrs["readonly"] = True
                    context["form"] = form
                    vars = main.models.VoteVariant.objects.filter(voting=voting)[:]
                    variants = []
                    for i in range(len(vars)):
                        variants.append((i, vars[i].description))
                    context["variants"] = variants
                context["addv_lock"] = addv_lock
                context["started"] = voting.started
                context["completed"] = voting.completed
            else:
                error = "У вас нет доступа к этому голосования!"
        result = (ok, error, success, form) if get_method else (ok, error, success)
        return result
    def post_handler(form, context, voting, addv_lock) -> (bool, str, bool):
        ferr = ok = False
        error = None
        if form.is_valid():
            action = form.data["action"]
            if action == "addv":
                ok, error = DB_VotingTools.try_add_vote_variant(request.user, voting, form.data["description"])
            elif action == "start":
                ok, error = DB_VotingTools.try_start_voting(request.user, voting)
                if ok:
                    addv_lock = True
            elif action == "stop":
                ok, error = DB_VotingTools.try_stop_voting(request.user, voting)
            else:
                ferr = True
        else:
            ferr = True
        if ferr:
            error = "Неверный формат отосланных данных!"
        return ok, error, addv_lock
    return view_func_template(request, "pages/voting_management/manage_voting.html", main.forms.ManageVotingForm, body, get_handler=body)