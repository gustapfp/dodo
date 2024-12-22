from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # -- ADMIN --
    path("admin/", admin.site.urls),
    # -- USER MANAGEMENT --
    path("accounts/", include("django.contrib.auth.urls")),
    # -- LOCAL APPS --
    path("users/", include("users.urls")),
    path("", include("pages.urls")),
]
