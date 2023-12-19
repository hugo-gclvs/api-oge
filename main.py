import os
from dotenv import load_dotenv
from services.session_manager import SessionManager
from services.oge_scraper import OgeScraper
from services.absence_service import AbsenceService

load_dotenv()

def main():
    session_manager = SessionManager(user=os.getenv("API_USERNAME"), pwd=os.getenv("API_PASSWORD"))
    
    # Connexion
    if session_manager.login():
        oge_scraper = OgeScraper(session_manager)

        absence_service = AbsenceService(oge_scraper)

        absences = absence_service.getAllAbsencesByClassroom("HS03")
        for absence in absences:
            print(absence)

        # absences = absence_service.getAllAbsencesBySubjectType("TD")
        # for absence in absences:
        #     print(absence)

        # absences = absence_service.getAllAbsences()
        # for absence in absences:
        #     print(absence)

    else:
        print("Error while logging in")

if __name__ == "__main__":
    main()
