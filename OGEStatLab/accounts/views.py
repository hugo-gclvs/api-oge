from django.contrib.auth import authenticate, login, logout
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
            return redirect('absences:home_page')
        else:
            return HttpResponse("Nom d'utilisateur ou mot de passe incorrect")
    elif request.user.is_authenticated:
        return redirect('absences:home_page')
    
    print(request.user.is_authenticated)

    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('accounts:login')