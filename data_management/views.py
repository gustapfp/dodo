from django.shortcuts import render
from django.views.generic import CreateView, TemplateView


class SortingFormView(TemplateView):
    template_name = "ONA/sorting_form.html"
    # model = Sorting1
    # fields = "__all__"
    # success_url = "/"
