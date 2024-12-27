from django.urls import path
from .views import SortingFormView

urlpatterns = [
    path("sorting", SortingFormView.as_view(), name="sorting_form")
]
