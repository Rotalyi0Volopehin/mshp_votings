from django import forms


class CommonFields:
    @staticmethod
    def get_voting_title_field(required, label="Название голосования"):
        return forms.CharField(label=label, min_length=1, max_length=256, required=required)

    @staticmethod
    def get_description_field(required, label="Описание"):
        return forms.CharField(widget=forms.Textarea, label=label, min_length=1, max_length=4096, required=required)

    @staticmethod
    def get_login_field(required, label="Логин"):
        return forms.CharField(label=label, min_length=1, max_length=32, required=required)

class RegistrationForm(forms.Form):
    login = CommonFields.get_login_field(True)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Пароль", min_length=1, max_length=32, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Повторите пароль", min_length=1, max_length=32, required=True)
    name = forms.CharField(label="Имя", min_length=1, max_length=32, required=True)
    email = forms.CharField(label="Email", min_length=1, max_length=32, required=True)


class NewVotingForm(forms.Form):
    title = CommonFields.get_voting_title_field(True, label="Название")
    description = CommonFields.get_description_field(False)
    type = forms.ChoiceField(label="Тип голосования", choices=((1, "0"), (2, "1"), (3, "2")), required=True)
    show_votes_before_end = forms.BooleanField(label="Показывать статистику голосов до окончания", required=False)
    anonymous = forms.BooleanField(label="Скрывать соответствие голосов и участников (анонимность)", required=False)


class AddVoteVariantForm(forms.Form):
    voting_title = CommonFields.get_voting_title_field(True)
    description = CommonFields.get_description_field(True, label="Описание варианта")


class RunVotingForm(forms.Form):
    voting_title = CommonFields.get_voting_title_field(True)
    action = forms.ChoiceField(label="Запрос на", widget=forms.RadioSelect(), choices=[(1, "начало"), (2, "завершение")], required=True)


class SearchVotingForm(forms.Form):
    author_login = CommonFields.get_login_field(True, "Логин автора")
    voting_title = CommonFields.get_voting_title_field(True)