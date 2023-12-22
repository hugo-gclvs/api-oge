from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect


def welcome_page(request):
    return HttpResponse("Bienvenue sur la page d'accueil de l'application web")

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Assurez-vous de passer l'objet 'user' ici
            return redirect('some-view-name')  # Rediriger vers la page souhaitée après la connexion
        else:
            return HttpResponse("Nom d'utilisateur ou mot de passe incorrect")

    return render(request, 'accounts/login.html')
