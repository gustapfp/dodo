from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("email", "username")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ("email", "username")

# class LoginForms(forms.Form):
#     login = forms.CharField(
#         label = "Nome de Login",
#         required = True,
#         max_length = 50
#     )
#     senha = forms.Charfield(
#         label="Senha",
#         required=True,
#         maz_length = 50
#     )