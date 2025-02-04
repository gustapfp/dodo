from django.contrib import admin
from django.urls import path, include
from users.views import login_view

urlpatterns = [
    # -- ADMIN --
    path("admin/", admin.site.urls),
    # -- USER MANAGEMENT --
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/login/", login_view, name="login"),
    # -- LOCAL APPS --
    path("users/", include("users.urls")),
    path("ona/", include("data_management.urls")),
    path("", include("pages.urls")),
]
