from django.contrib.auth import login
from django.http import HttpResponse
from django.shortcuts import render, redirect

from services.session_manager import SessionManager


def welcome_page(request):
    return HttpResponse("Bienvenue sur la page d'accueil de l'application web")

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            request.session['oge_user'] = username
            request.session['oge_password'] = password
            
            login(request, user)
            return redirect('welcome_page')
        else:
            return HttpResponse("Nom d'utilisateur ou mot de passe incorrect")

    return render(request, 'accounts/login.html')

def logout_view(request):
    request.session.flush()
    return redirect('login_view')