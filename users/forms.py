from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import Hospital, CODEMember

class CODEMemberCreationForm(UserCreationForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )
    class Meta:
        model = CODEMember
        fields = ("email", "is_admin")
    
    def clean_passoword2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()


class CODEMemberChangeForm(UserChangeForm):
    class Meta:
        model = CODEMember
        fields = ("email", "password","is_active", "is_admin")





class HospitalCreationForm(UserCreationForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )
    class Meta:
        model = Hospital
        fields = ("username", "email", "contact_number", "address", "sectors")



    def clean_passoword2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()

class HospitalChangeForm(UserChangeForm):
    class Meta:
        model = Hospital
        fields =  ("username","password",  "email", "contact_number", "address","is_active", "sectors", "last_service")
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