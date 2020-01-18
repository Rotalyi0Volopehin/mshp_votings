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


def vote_page(request):
    context = {
        'menu': get_menu_context()
    }
    return render(request, 'pages/vote.html', context)
