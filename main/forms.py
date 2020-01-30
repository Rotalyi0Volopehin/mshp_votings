from django import forms


class CommonFields:
    @staticmethod
    def get_voting_title_field(required, label="Название голосования", attrs=None):
        if attrs is None:
            return forms.CharField(label=label, min_length=1, max_length=256, required=required)
        return forms.CharField(label=label, min_length=1, max_length=256, required=required, widget=forms.TextInput(attrs=attrs))

    @staticmethod
    def get_description_field(required, label="Описание", attrs=None):
        if attrs is None:
            return forms.CharField(widget=forms.Textarea, label=label, min_length=1, max_length=4096, required=required)
        return forms.CharField(widget=forms.Textarea(attrs=attrs), label=label, min_length=1, max_length=4096, required=required)

    @staticmethod
    def get_login_field(required, label="Логин"):
        return forms.CharField(label=label, min_length=1, max_length=32, required=required)

    @staticmethod
    def get_name_field(required, label="Имя"):
        return forms.CharField(label=label, min_length=1, max_length=64, required=required)

    @staticmethod
    def get_password_field(required, label="Пароль"):
        return forms.CharField(widget=forms.PasswordInput, label=label, min_length=1, max_length=64, required=required)

    @staticmethod
    def get_filter_option_field(label):
        return forms.ChoiceField(label=label, required=False,
                choices=[(0, "--- (0)"), (1, "исключение (1)"), (-1, "исключение иных (-1)")])

    @staticmethod
    def get_invisible_field(type_, id, value=''):
        return type_(label="", widget=forms.HiddenInput(attrs={ "id": id, "value": value }))


class RegistrationForm(forms.Form):
    login = CommonFields.get_login_field(True)
    password1 = CommonFields.get_password_field(True)
    password2 = CommonFields.get_password_field(True, "Повторите пароль")
    name = CommonFields.get_name_field(True)
    email = forms.CharField(label="E-mail", min_length=1, max_length=64, required=True)


class NewVotingForm(forms.Form):
    title = CommonFields.get_voting_title_field(True, label="Название", attrs={"class": "form-control col-sm-9"})
    description = CommonFields.get_description_field(False, attrs={"class": "w-100"})
    type = forms.ChoiceField(label="Тип голосования", choices=((0, "0"), (1, "1"), (2, "2")), required=True)
    show_votes_before_end = forms.BooleanField(label="Показывать статистику голосов до окончания", required=False)
    anonymous = forms.BooleanField(label="Скрывать соответствие голосов и участников (анонимность)", required=False)


class AddVoteVariantForm(forms.Form):
    voting_title = CommonFields.get_voting_title_field(True)
    description = CommonFields.get_description_field(True, label="Описание варианта")


class VoteForm(forms.Form):
    answer = forms.CharField(label="", min_length=1, required=True, widget=forms.HiddenInput(attrs={ "id": "answer_tag" }))


class SearchVotingForm(forms.Form):
    author_login = CommonFields.get_login_field(False, "Логин автора")
    voting_title = CommonFields.get_voting_title_field(False)
    started_option = CommonFields.get_filter_option_field("Фильтрация начатых")
    completed_option = CommonFields.get_filter_option_field("Фильтрация законченных")
    show_votes_before_end_option = CommonFields.get_filter_option_field("Фильтрация показывающих статистику до завершения")
    anonymous_option = CommonFields.get_filter_option_field("Фильтрация анонимных")
    offset = CommonFields.get_invisible_field(forms.IntegerField, "offset_tag", 0)


class ManageVotingForm(forms.Form):
    description = CommonFields.get_description_field(False, label="Описание варианта", attrs={"class": "w-100", "rows": "20"})
    action = CommonFields.get_invisible_field(forms.CharField, "action_tag", '')


class ProfileForm(forms.Form):
    name = CommonFields.get_name_field(False)
    about = CommonFields.get_description_field(False, label="О себе")
    password = CommonFields.get_password_field(False)
    new_password1 = CommonFields.get_password_field(False)
    new_password2 = CommonFields.get_password_field(False)
    action = CommonFields.get_invisible_field(forms.CharField, "action_tag", '')