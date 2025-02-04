from django.urls import path
from .views import ONAFormView, EvaluatorView

urlpatterns = [
    path("evaluator", EvaluatorView.as_view(), name="evaluator_form"),
    path(
        "form/<int:hospital_id>/<int:evaluator_id>",
        ONAFormView.as_view(),
        name="ona_form",
    ),
]
