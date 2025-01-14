from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from .forms import CODEMemberCreationForm, CODEMemberChangeForm, HospitalCreationForm, HospitalChangeForm
from .models import CODEMember, Hospital, Sector
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

admin.site.unregister(Group)
admin.site.register(Sector)

@admin.register(CODEMember)
class CODEMemberAdmin(UserAdmin):
    add_form = CODEMemberCreationForm
    form = CODEMemberChangeForm

    fieldsets = (
        (None, {
            "fields": ("username", "password",)
            }
        ),
        ("Permissions", {
            "fields": ("is_active", "is_staff", "is_superuser",)
            }
        ),
    )

    add_fieldsets =  (
        None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_staff', 'is_superuser',),
        }),

    list_display = ("username", "is_staff", "is_superuser",)
    list_display_links = ("username",)
    list_editable = ("is_staff", "is_superuser",)
    
    


@admin.register(Hospital)
class HospitalAdmin(UserAdmin):
    add_form = HospitalCreationForm
    form = HospitalChangeForm

    fieldsets = (
        (
            None, {"fields": ("username", "password")}
        ),
        (
            "Details", {"fields": ( "email", "contact_number", "address", "sectors",)}
        ),
        (
            "Permissions", {"fields": ("is_active",)}
        ),

    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_active'),
        }),
    )
    list_display = ("username", "is_active", "email",)
    list_display_links = ("username", "email",)
    search_fields = ("username",)
    list_filter = ("is_active",)
    list_editable = ("is_active",)
    filter_horizontal = ["sectors"]

    def has_module_permission(self, request):
        """Restrict `Hospital` users from accessing the admin."""
        return request.user.is_superuser or request.user.is_staff
