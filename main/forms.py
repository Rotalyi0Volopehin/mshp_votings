from django import forms


class RegistrationForm(forms.Form):
    login = forms.CharField(label="Логин", min_length=1, max_length=32, required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Пароль", min_length=1, max_length=32, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Повторите пароль", min_length=1, max_length=32, required=True)
    name = forms.CharField(label="Имя", min_length=1, max_length=32, required=True)
    email = forms.CharField(label="Email", min_length=1, max_length=32, required=True)


class NewVotingForm(forms.Form):
    title = forms.CharField(label="Название", min_length=1, max_length=256, required=True)
    description = forms.CharField(widget=forms.Textarea, label="Описание", max_length=4096, required=False)
    type = forms.ChoiceField(label="Тип голосования", choices=((1, "0"), (2, "1"), (3, "2")), required=True)
    show_votes_before_end = forms.BooleanField(label="Показывать статистику голосов до окончания", required=False)
    anonymous = forms.BooleanField(label="Скрывать соответствие голосов и участников", required=False)


class AddVoteVariantForm(forms.Form):
    voting_title = forms.CharField(label="Название голосования", min_length=1, max_length=256, required=True)
    description = forms.CharField(widget=forms.Textarea, label="Описание варианта", min_length=1, max_length=4096)