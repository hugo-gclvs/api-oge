from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect


def welcome_page(request):
    return HttpResponse("Bienvenue sur la page d'accueil de l'application web")

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            request.session['oge_user'] = username
            request.session['oge_password'] = password
            
            login(request, user)
            return redirect('absences:welcome_page')
        else:
            return HttpResponse("Nom d'utilisateur ou mot de passe incorrect")

    return render(request, 'accounts/login.html')

def logout_view(request):
    request.session.flush()
    return redirect('accounts:login')