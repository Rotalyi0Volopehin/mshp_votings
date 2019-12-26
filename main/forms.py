from django import forms


class RegistrationForm(forms.Form):
    login = forms.CharField(label="Login", min_length=1, max_length=32, required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password", min_length=1, max_length=32, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Repeat password", min_length=1, max_length=32, required=True)
    name = forms.CharField(label="Name", min_length=1, max_length=32, required=True)
    email = forms.CharField(label="Email", min_length=1, max_length=32, required=True)