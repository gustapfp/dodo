from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUSerCreationForm, CustomMemberChangeForm
from .models import CustomUser

admin.site.unregister(Group)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUSerCreationForm
    form = CustomMemberChangeForm
    model = CustomUser  # ensures admin knows which model we're managing

    # When viewing/editing an existing user
    fieldsets = (
        (None, {
            "fields": ("username", "password", "role",),
        }),
        ("Permissions", {
            "fields": ("is_active", "is_staff", "is_superuser",),
        }),
    )

    # When creating a new user
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "role", "password1", "password2", 
                           "is_staff", "is_superuser"),
            },
        ),
    )

    list_display = ("username", "role", "is_staff", "is_superuser")
    list_display_links = ("username",)
    # Optional: make fields editable directly from the list view
    list_editable = ("role", "is_staff", "is_superuser",)
    


