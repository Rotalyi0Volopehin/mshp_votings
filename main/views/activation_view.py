from main.db_tools.db_user_tools import DB_UserTools
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.http import HttpResponse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from main.db_tools.tokens import account_activation_token
from django.shortcuts import render


def activate(request, uid, token):
    if request.method == "GET":
        try:
            uid = force_text(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if (user != None) and account_activation_token.check_token(user, token):
            if DB_UserTools.try_activate_user(user):
                login(request, user)
            return render(request, 'registration/activation.html')
        return HttpResponse('Ссылка для верификации невалидна!')