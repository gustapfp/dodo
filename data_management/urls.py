from django.urls import path
from .views import OnaFormView, EvaluatorView

urlpatterns = [
    path("evaluator", EvaluatorView.as_view(), name="evaluator_form"), 
    path("ona", OnaFormView.as_view(), name="ona_form")
]
