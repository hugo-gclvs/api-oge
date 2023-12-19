import os
from dotenv import load_dotenv
from services.session_manager import SessionManager
from services.oge_scraper import OgeScraper
from services.absence_service import AbsenceService
# from services.grade_service import GradeService

load_dotenv()

def main():
    # Création de l'instance de SessionManager avec les identifiants
    print(os.getenv("API_USERNAME"))

    session_manager = SessionManager(user=os.getenv("API_USERNAME"), pwd=os.getenv("API_PASSWORD"))
    
    # Connexion
    if session_manager.login():
        # Initialisation de OgeScraper avec SessionManager
        oge_scraper = OgeScraper(session_manager)

        # Initialisation des services avec OgeScraper
        absence_service = AbsenceService(oge_scraper)
        # grade_service = GradeService(oge_scraper)

        # Récupération des absences
        absences = absence_service.getAllAbsences()
        for absence in absences:
            print(absence)  # Assurez-vous que la méthode __str__ est bien définie dans le modèle d'absence

        # Récupération des notes (exemple, implémentez selon vos besoins)
        # grades = grade_service.getGrades(semester)

    else:
        print("Échec de la connexion.")

if __name__ == "__main__":
    main()
