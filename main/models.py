import datetime

from django.contrib.auth.models import User
from django.db import models


def get_sentinel_user():
    return User.objects.get_or_create(username='deleted')[0]


#class User:
    # first_name - имя
    # email - email
    # username - логин
    # password - хэш пароля
    # date_joined - дата регистрации


class UserData(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    activated = models.BooleanField(default=False)
    extra_info = models.TextField(default='')


class VotingSet(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.SET(get_sentinel_user))
    title = models.TextField(default='')
    description = models.TextField(default='')
    date_created = models.DateTimeField(default=datetime.datetime.now(), blank=True)


class VotingSetAccess(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    set = models.ForeignKey(to=VotingSet, on_delete=models.CASCADE)


class Voting(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.SET(get_sentinel_user))
    set = models.ForeignKey(to=VotingSet, on_delete=models.CASCADE)
    title = models.TextField(default='')
    description = models.TextField(default='')
    type = models.IntegerField(default=0)
    show_votes_before_end = models.BooleanField(default=False)
    anonymous = models.BooleanField(default=True)
    started = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=datetime.datetime.now(), blank=True)
    date_started = models.DateTimeField(default=datetime.datetime.now(), blank=True)
    date_stopped = models.DateTimeField(default=datetime.datetime.now(), blank=True)


class VoteVariant(models.Model):
    voting = models.ForeignKey(to=Voting, on_delete=models.CASCADE)
    description = models.TextField(default='')
    vote_fact_count = models.IntegerField(default=0) #значение увеличивается во время голосования; поле для оптимизации подсчёта голосов


class VoteFact(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET(get_sentinel_user))
    voting = models.ForeignKey(to=Voting, on_delete=models.CASCADE)
    answer = models.BigIntegerField(default=0)


class VotingAbuse(models.Model):
    abuser = models.ForeignKey(to=User, on_delete=models.SET(get_sentinel_user))
    voting = models.ForeignKey(to=Voting, on_delete=models.CASCADE)
    description = models.TextField(default='')