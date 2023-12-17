from django.shortcuts import render
from django.http import HttpResponse
from .services.OgeAPI import OgeAPI

def welcome_page(request):
    return HttpResponse("Bienvenue sur la page d'accueil de l'application web")

def get_all_absences(request):
    api = OgeAPI()
    api.login()

    try:
      absences = api.getAllAbsences()
    except Exception as e:
      absences = []

    return render(request, 'webApp/get_all_absences.html', {'absences': absences})