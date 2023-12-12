import re
import requests
from bs4 import BeautifulSoup
import os
import logging
from utils import data_processing
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

class OgeAPI:
    def __init__(self, user=os.getenv("API_USERNAME"), pwd=os.getenv("API_PASSWORD")):
        self.username = user
        self.password = pwd
        self.session = requests.Session()
        self.initialize_urls()

    def initialize_urls(self):
        self.home_url = "https://iutdijon.u-bourgogne.fr/oge-esirem/"
        self.login_url = "https://casiut21.u-bourgogne.fr/cas-esirem/login?service=https%3A%2F%2Fiutdijon.u-bourgogne.fr%2Foge-esirem%2F"
        self.absences_url = "https://iutdijon.u-bourgogne.fr/oge-esirem/stylesheets/etu/absencesEtu.xhtml"
        self.grades_url = "https://iutdijon.u-bourgogne.fr/oge-esirem/stylesheets/etu/bilanEtu.xhtml"

    def login(self):
        try:
            execution = self._get_execution_token(self.login_url)
            return self._perform_login(execution)
        except Exception as e:
            logging.error(f"Login failed: {e}")
            return False
        
    def _get_execution_token(self, url):
        response = self.session.get(url, timeout=5)
        return re.search(r'name="execution" value="([^"]+)"', response.text).group(1)

    def _perform_login(self, execution):
        payload = {
            'username': self.username,
            'password': self.password,
            'execution': execution,
            '_eventId': 'submit'
        }
        response = self.session.post(self.login_url, data=payload, timeout=5)
        if "Connexion - CAS" not in response.text:
            logging.info("Login successful")
            return True
        logging.error("Login failed")
        return False
    
    def get(self, url):
        print(f"Get {url}")
        return self.session.get(url)

    def getAbsencesPage(self):
        print("Get absences page...")
        response = self.session.get(self.absences_url)
        return response.text
    
    def getGradesPage(self):
        print("Get grades page...")
        response = self.session.get(self.grades_url)
        return response.text
    
    def getAbsences(self, semester):
        absencesPage = self._selectAbsencesSemester(semester)
        return data_processing.create_absences(absencesPage) if absencesPage else []

    def _selectAbsencesSemester(self, semester):
        try:
            response = self.session.post(self.absences_url, headers=self._get_headers(), data=self._get_absences_data(semester), timeout=5)
            return self._extract_content(response)
        except Exception as e:
            logging.error(f"Error in selecting absences semester: {e}")
            return None
        
    def _extract_content(self, response):
        content = response.text.split("![CDATA[")[1].split("]]")[0]
        return content
        
    def _get_headers(self):
        return {
            "Faces-Request": "partial/ajax",
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }
    
    def _get_absences_data(self, semester):
        return {
            "javax.faces.partial.ajax": "true",
            "javax.faces.source": "ficheEtudiantForm:j_id_16_" + str(semester),
            "javax.faces.partial.execute": "@all",
            "javax.faces.partial.render": "ficheEtudiantForm:panel",
            "ficheEtudiantForm:j_id_16_" + str(semester): "ficheEtudiantForm:j_id_16_" + str(semester),
            "ficheEtudiantForm_SUBMIT": "1",
            "javax.faces.ViewState": "0"
        }

    def selectGradesSemester(self, semester):
        headers = {
            "Faces-Request": "partial/ajax",
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }

        data = {
            "javax.faces.partial.ajax": "true",
            "javax.faces.source": "mainBilanForm:j_id_15",
            "javax.faces.partial.execute": "mainBilanForm:j_id_15",
            "javax.faces.partial.render": "mainBilanForm",
            "mainBilanForm:j_id_15": "mainBilanForm:j_id_15",
            "i": str(int(semester) - 1),
            "mainBilanForm:j_id_15_menuid": str(int(semester) - 1),
            "mainBilanForm_SUBMIT": "1",
            "javax.faces.ViewState": "0"
        }

        # Send the request
        response = self.session.post(self.grades_url, headers=headers, data=data)

        # Process the response to extract the real content
        content = response.text.split("![CDATA[")[1].split("]]")[0]

        return content
    
    def getGrades(self, semester):
        gradesPage = self.selectGradesSemester(semester)

        soup = BeautifulSoup(gradesPage, 'html.parser')

        # To do later...

        grades = []

        return grades
