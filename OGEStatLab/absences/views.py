from django.http import HttpResponse
from django.shortcuts import render

def welcome_page(request):
    return HttpResponse("Bienvenue sur la page d'accueil de l'application web")
