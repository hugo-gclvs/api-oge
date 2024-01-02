from django.contrib.auth import authenticate, login
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
        print("username: ", username)
        print("password: ", password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Connexion avec le système Django

            # Ici, vous initialisez votre session personnalisée
            session_manager = SessionManager(user=username, password=password)
            if session_manager.login():
                request.session['oge_session'] = session_manager  # Stockez votre session_manager dans la session Django
                return redirect('some-view-name')
            else:
                return HttpResponse("Échec de la connexion au service OGE")

        else:
            return HttpResponse("Nom d'utilisateur ou mot de passe incorrect")

    return render(request, 'accounts/login.html')