from django.urls import path 
from .views import user_page_view


urlpatterns = [
    path("", user_page_view, name="users")
]
