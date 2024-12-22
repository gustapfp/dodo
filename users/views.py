from django.shortcuts import render
# from .forms import LoginForms
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            messages.error(request, 'Invalid username or password')
    return render(
        request=request,
        template_name= "templates/registration/login.html",
        )