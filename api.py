import re
import requests
from bs4 import BeautifulSoup
from getpass import getpass
from dotenv import load_dotenv
import os

load_dotenv()

class API:
    def __init__(self, user=os.getenv("API_USERNAME"), pwd=os.getenv("API_PASSWORD")):
        self.username = user
        self.password = pwd
        self.home_url = "https://iutdijon.u-bourgogne.fr/oge-esirem/"
        self.login_url = "https://casiut21.u-bourgogne.fr/cas-esirem/login?service=https%3A%2F%2Fiutdijon.u-bourgogne.fr%2Foge-esirem%2F"
        self.absences_url = "https://iutdijon.u-bourgogne.fr/oge-esirem/stylesheets/etu/absencesEtu.xhtml"
        self.grades_url = "https://iutdijon.u-bourgogne.fr/oge-esirem/stylesheets/etu/bilanEtu.xhtml"
        self.session = requests.Session()

        print(f"API created")

    def get(self, url):
        print(f"Get {url}")
        return self.session.get(url)

    def login(self):
        response = self.session.get(self.login_url)
        execution = re.search(r'name="execution" value="([^"]+)"', response.text).group(1)
        payload = {
            'username': self.username,
            'password': self.password,
            'execution': execution,
            '_eventId': 'submit'
        }
        login_response = self.session.post(self.login_url, data=payload)



        if "Connexion - CAS" not in login_response.text:
            print("Login successful")
            return True
        else:
            print("Login failed")
            return False

    def getAbsencesPage(self):
        print("Get absences page...")
        response = self.session.get(self.absences_url)
        return response.text
    
    def getGradesPage(self):
        print("Get grades page...")
        response = self.session.get(self.grades_url)
        return response.text
    
    def getAbsences(self):
        test = self.select_semester(1)
        print(test)

        page = self.getAbsencesPage()
        soup = BeautifulSoup(page, 'html.parser')

        absences_table = soup.find_all('tr', class_='ui-widget-content')
        print(f"Found {len(absences_table)} absences")

        absences = []
        for row in absences_table:
            columns = row.find_all('td', class_='ui-panelgrid-cell')
            absence_data = [column.get_text(strip=True) for column in columns]
            absences.append(absence_data)

        return absences

    def getGrades(self):
        test = self.select_semester(1)

        # page = self.getGradesPage()
        # soup = BeautifulSoup(page, 'html.parser')

        # print(soup)

        # non_empty_gridcells = soup.find_all(lambda tag: tag.name == 'td' and tag.get('role') == 'gridcell' and tag.text.strip())
        # print(f"Found {(len(non_empty_gridcells)/2)-1} grades")

        grades = []

        return grades

    def select_semester(self, semester):
        headers = {
            "Faces-Request": "partial/ajax",
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }

        data = {
            "javax.faces.partial.ajax": "true",
            "javax.faces.source": "mainBilanForm%j_id_15", #mainBilanForm:j_id_15
            "javax.faces.partial.execute": "mainBilanForm%j_id_15",
            "javax.faces.partial.render": "mainBilanForm",
            "mainBilanForm%j_id_15": "mainBilanForm%j_id_15",
            "i": str(int(semester) - 1),
            "mainBilanForm%3Aj_id_1t_menuid": str(int(semester) - 1),
            "mainBilanForm_SUBMIT": "1",
            "javax.faces.ViewState": "0"
        }

        response = self.session.post(self.absences_url, headers=headers, data=data)
        print(response.text)
        # Process the response to extract the real content
        # content = response.text.split("![CDATA[")[1].split("]]")[0]

        # print(content)

        return response
