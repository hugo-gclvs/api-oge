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
    """
    This class is used to interact with the OGE API.
    
    Attributes:
        username (str): The username used to connect to the OGE.
        password (str): The password used to connect to the OGE.
        session (requests.Session): The session used to send requests to the OGE.
        home_url (str): The URL of the OGE home page.
        login_url (str): The URL of the OGE login page.
        absences_url (str): The URL of the OGE absences page.
        grades_url (str): The URL of the OGE grades page.
    """
    def __init__(self, user=os.getenv("API_USERNAME"), pwd=os.getenv("API_PASSWORD")):
        """
        The constructor for the OgeAPI class.
        
        Parameters:
            user (str): The username used to connect to the OGE.
            pwd (str): The password used to connect to the OGE.
            
        Returns:
            None
        """
        self.username = user
        self.password = pwd
        self.session = requests.Session()
        self.initialize_urls()

    def initialize_urls(self):
        """
        This method initializes the URLs used to interact with the OGE.

        Parameters:
            None

        Returns:
            None
        """
        self.home_url = "https://iutdijon.u-bourgogne.fr/oge-esirem/"
        self.login_url = "https://casiut21.u-bourgogne.fr/cas-esirem/login?service=https%3A%2F%2Fiutdijon.u-bourgogne.fr%2Foge-esirem%2F"
        self.absences_url = "https://iutdijon.u-bourgogne.fr/oge-esirem/stylesheets/etu/absencesEtu.xhtml"
        self.grades_url = "https://iutdijon.u-bourgogne.fr/oge-esirem/stylesheets/etu/bilanEtu.xhtml"

    def login(self):
        """
        This method is used to login to the OGE.

        Parameters:
            None

        Returns:
            bool: True if the login was successful, False otherwise.
        """
        try:
            execution = self._get_execution_token(self.login_url)
            return self._perform_login(execution)
        except Exception as e:
            logging.error(f"Login failed: {e}")
            return False
        
    def _get_execution_token(self, url):
        """
        This method is used to get the execution token from the OGE login page.

        Parameters:
            url (str): The URL of the OGE login page.

        Returns:
            str: The execution token.
        """
        response = self.session.get(url, timeout=5)
        return re.search(r'name="execution" value="([^"]+)"', response.text).group(1)

    def _perform_login(self, execution):
        """
        This method is used to perform the login to the OGE.

        Parameters:
            execution (str): The execution token.

        Returns:
            bool: True if the login was successful, False otherwise.
        """
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
        """
        This method is used to send a GET request to the OGE.
        
        Parameters:
            url (str): The URL of the request.
            
        Returns:
            requests.Response: The response of the request.
        """
        print(f"Get {url}")
        return self.session.get(url)

    def getAbsencesPage(self):
        """
        This method is used to get the absences page from the OGE.

        Parameters:
            None

        Returns:
            str: The absences page.
        """
        print("Get absences page...")
        response = self.session.get(self.absences_url)
        return response.text
    
    def getGradesPage(self):
        """
        This method is used to get the grades page from the OGE.

        Parameters:
            None
            
        Returns:
            str: The grades page.
        """
        print("Get grades page...")
        response = self.session.get(self.grades_url)
        return response.text
    
    def getAllAbsences(self):
        """
        This method is used to get the absences from the OGE.

        Parameters:
            semester (int): The semester to get the absences from.

        Returns:
            list: The absences.
        """
        semesters = self._countSemesters()

        absences = []
        for semester in range(1, semesters + 1):
            absencesPage = self._fetchAbsencesForSemester(semester)
            absences += data_processing.create_absences(absencesPage) if absencesPage else []

        return absences
    
    def _countSemesters(self):
        """
        This method is used to count the number of semesters.

        Parameters:
            None

        Returns:
            int: The number of semesters.
        """
        try:
            minSemester = self._getMinSemester()
            maxSemester = self._getMaxSemester()
            return maxSemester - minSemester + 1
        except Exception as e:
            logging.error(f"Error in counting semesters: {e}")
            return 0
        
    def _getMinSemester(self):
        """
        This method is used to get the minimum semester.

        Parameters:
            None

        Returns:
            int: The minimum semester.
        """
        try:
            absencesPage = self.getAbsencesPage()
            soup = BeautifulSoup(absencesPage, 'html.parser')
            min_semester_text = soup.find('span', class_='ui-menuitem-text').get_text()
            min_semester = int(min_semester_text.split()[-1])
            return min_semester
        except Exception as e:
            logging.error(f"Error in getting min semester: {e}")
            return 0
        
    def _getMaxSemester(self):
        """
        This method is used to get the maximum semester.

        Parameters:
            None

        Returns:
            int: The maximum semester.
        """
        try:
            absencesPage = self.getAbsencesPage()
            soup = BeautifulSoup(absencesPage, 'html.parser')
            max_semester_text = soup.find_all('span', class_='ui-menuitem-text')[-1].get_text()
            max_semester = int(max_semester_text.split()[-1])
            return max_semester
        except Exception as e:
            logging.error(f"Error in getting max semester: {e}")
            return 0

    def _fetchAbsencesForSemester(self, semester):
        """
        This method is used to select the absences semester.

        Parameters:
            semester (int): The semester to select.

        Returns:
            str: The absences page.
        """
        try:
            response = self.session.post(self.absences_url, headers=self._get_headers(), data=self._get_absences_data(semester), timeout=5)
            return self._extract_content(response)
        except Exception as e:
            logging.error(f"Error in selecting absences semester: {e}")
            return None
        
    def _extract_content(self, response):
        """
        This method is used to extract the content from the response.

        Parameters:
            response (requests.Response): The response to process.

        Returns:
            str: The content.
        """
        content = response.text.split("![CDATA[")[1].split("]]")[0]
        return content
        
    def _get_headers(self):
        """
        This method is used to get the headers for the request.

        Parameters:
            None

        Returns:
            dict: The headers.
        """
        return {
            "Faces-Request": "partial/ajax",
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }
    
    def _get_absences_data(self, semester):
        """
        This method is used to get the data for the request.

        Parameters:
            semester (int): The semester to select.

        Returns:
            dict: The data.
        """
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
