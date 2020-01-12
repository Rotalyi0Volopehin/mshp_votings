import datetime

from django.shortcuts import render


def get_menu_context():
    return [
        {'url': '/', 'name': 'Главная'},
        {'url': '/voting/', 'name': 'Опросы'},
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


def vote_create_page(request):
    context = {
        'pagename': 'Создание голосование',
        'menu': get_menu_context()
    }
    return render(request, 'pages/vote_create.html', context)


def option_create_page(request):
    context = {
        'pagename': 'Добавление варианта',
        'menu': get_menu_context()
    }
    return render(request, 'pages/option_create.html', context)
