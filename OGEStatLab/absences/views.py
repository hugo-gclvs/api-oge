from django.http import HttpResponse, JsonResponse
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
    if not session_manager.login():
        return HttpResponse("Erreur de connexion")

    oge_scraper = OgeScraper(session_manager)
    absence_service = AbsenceService(oge_scraper)

    # Vérifier si la requête est une requête AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        filter_type = request.GET.get('filterType')
        filter_value = request.GET.get('filterValue')

        try:
            if(filter_type == 'null'):
                absences = absence_service.getAllAbsences()
            if(filter_type == 'teacher'):
                absences = absence_service.getAbsencesByTeacher(filter_value)
            if(filter_type == 'subjectType'):
                absences = absence_service.getAllAbsencesBySubjectType(filter_value)
            if(filter_type == 'classroom'):
                absences = absence_service.getAllAbsencesByClassroom(filter_value)

            # Convertir les objets Absence en dictionnaires
            absences_data = [absence.to_dict() for absence in absences]
        except Exception as e:
            return JsonResponse({'error': str(e)})

        # Retourner les données filtrées en format JSON
        return JsonResponse({'absences': absences_data})

    # Pour les requêtes non-AJAX, obtenir toutes les absences
    try:
        absences = absence_service.getAllAbsences()
    except Exception as e:
        absences = []

    return render(request, 'absences/get_all_absences.html', {'absences': absences})

def get_all_teachers(request):
    session_manager = SessionManager(user=os.getenv("API_USERNAME"), pwd=os.getenv("API_PASSWORD"))
    
    if not session_manager.login():
        return JsonResponse({'error': 'Erreur de connexion'}, status=401)

    oge_scraper = OgeScraper(session_manager)
    absence_service = AbsenceService(oge_scraper)

    try:
        teachers = absence_service.getAllTeachersAbsences()
        # Supposons que teachers soit une liste de chaînes
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'teachers': teachers})

def get_all_classrooms(request):
    session_manager = SessionManager(user=os.getenv("API_USERNAME"), pwd=os.getenv("API_PASSWORD"))
    
    if not session_manager.login():
        return JsonResponse({'error': 'Erreur de connexion'}, status=401)

    oge_scraper = OgeScraper(session_manager)
    absence_service = AbsenceService(oge_scraper)

    try:
        classrooms = absence_service.getAllClassroomsAbsences()
        # Supposons que subject_types soit une liste de chaînes
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'classrooms': classrooms})