from django.shortcuts import render
from django.http import HttpResponse
from .services.OgeAPI import OgeAPI

def afficher_donnees(request):
    # Logique pour récupérer et traiter les données
    donnees = "Contenu des données"
    return HttpResponse(donnees)

def afficher_absences(request):
    api = OgeAPI()
    api.login()

    try:
      absences = api.getAllAbsences()
    except Exception as e:
      absences = []

    return render(request, 'webApp/afficher_absences.html', {'absences': absences})