import re
import requests
from bs4 import BeautifulSoup
from getpass import getpass

class API:
    def __init__(self, user=input("Username: "), pwd=getpass("Password: ")):
        self.username = user
        self.password = pwd
        self.home_url = "https://iutdijon.u-bourgogne.fr/oge-esirem/"
        self.login_url = "https://casiut21.u-bourgogne.fr/cas-esirem/login?service=https%3A%2F%2Fiutdijon.u-bourgogne.fr%2Foge-esirem%2F"
        self.absences_url = "https://iutdijon.u-bourgogne.fr/oge-esirem/stylesheets/etu/absencesEtu.xhtml"
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

    def getAbsences(self):
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
