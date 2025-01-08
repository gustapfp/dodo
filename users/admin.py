from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CODEMember, Hospital



admin.site.unregister(User)


class UserCODEMemberAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CODEMember
    list_display = [
        "email",
        "username",
        "is_superuser",
    ]


admin.site.register(CODEMember, UserCODEMemberAdmin)
