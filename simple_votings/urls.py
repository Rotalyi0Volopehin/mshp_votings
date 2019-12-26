"""simple_votings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from main import views
from django.contrib.auth import views as auth_views

from main.views import get_menu_context

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_page),
    path('time/', views.time_page),
    path('login/', views.login_cloak), #из-за хэширования пароля необходима эта надстройка
    path('logout/', auth_views.LogoutView.as_view()),
    path('registration/', views.registration_page),
    path('cul/', views.clear_user_list_page), #страница, удаляющая всех пользователей
]
