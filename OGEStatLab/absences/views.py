from django.http import HttpResponse
from django.shortcuts import render
from dotenv import load_dotenv
from services.session_manager import SessionManager
from services.oge_scraper import OgeScraper
from services.absence_service import AbsenceService
import os

load_dotenv()

def welcome_page(request):
    return HttpResponse("Bienvenue sur la page d'accueil de l'application web")

def get_all_absences(request):
    session_manager = SessionManager(user=os.getenv("API_USERNAME"), pwd=os.getenv("API_PASSWORD"))
    
    # Connexion
    if session_manager.login():
        oge_scraper = OgeScraper(session_manager)

        absence_service = AbsenceService(oge_scraper)

        try:
            absences = absence_service.getAllAbsences()
        except Exception as e:
            absences = []

    return render(request, 'absences/get_all_absences.html', {'absences': absences})