from dotenv import load_dotenv
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import os

from services.session_manager import SessionManager
from services.oge_scraper import OgeScraper
from services.absence_service import AbsenceService

load_dotenv()

def create_service():
    session_manager = SessionManager(user=os.getenv("API_USERNAME"), pwd=os.getenv("API_PASSWORD"))
    if not session_manager.login():
        return None
    oge_scraper = OgeScraper(session_manager)
    return AbsenceService(oge_scraper)

def welcome_page(request):
    return HttpResponse("Bienvenue sur la page d'accueil de l'application web")

def get_all_absences(request):
    absence_service = create_service()
    if not absence_service:
        return HttpResponse("Error while logging in", status=401)

    teacher_filter = request.GET.get('teacher')
    classroom_filter = request.GET.get('classroom')
    subject_type_filter = request.GET.get('subjectType')

    try:
        absences = absence_service.getAbsencesWithMultipleFilters(
            teacher=teacher_filter,
            classroom=classroom_filter,
            subjectType=subject_type_filter
        )
        absences_data = [absence.to_dict() for absence in absences]
    except Exception as e:
        return JsonResponse({'error': str(e)})

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'absences': absences_data})

    return render(request, 'absences/get_all_absences.html', {'absences': absences_data})



def get_all_teachers(request):
    return get_absence_data('getAllTeachersAbsences')

def get_all_classrooms(request):
    return get_absence_data('getAllClassroomsAbsences')

def get_absence_data(method_name):
    absence_service = create_service()
    if not absence_service:
        return JsonResponse({'error': 'Erreur de connexion'}, status=401)

    try:
        data = getattr(absence_service, method_name)()
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({method_name.lower(): data})
