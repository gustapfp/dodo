from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def user_page_view(request):
    return HttpResponse("Hello, World! user app")
