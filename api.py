import re
from getpass import getpass
import requests
from bs4 import BeautifulSoup


class API:
    def __init__(self, user=input("Username: "), pwd=getpass("Password: ")):
        self.username = user
        self.pwd = pwd
        self.URL_ACCUEIL = "https://iutdijon.u-bourgogne.fr/oge-esirem/"
        self.URL_LOGIN = "https://casiut21.u-bourgogne.fr/cas-esirem/login?service=https%3A%2F%2Fiutdijon.u-bourgogne.fr%2Foge-esirem%2F"
        self.URL_ABSENCES = "https://iutdijon.u-bourgogne.fr/oge-esirem/stylesheets/etu/absencesEtu.xhtml"
        self.session = requests.Session()

        print("API created")
        print("User: " + self.username)
        print("Password: " + self.pwd)
    
    def get(self, url):
        print("Get " + url)
        return self.session.get(url)
    
    def login(self):
        # GET request to fetch login form
        response = self.session.get(self.URL_LOGIN)
        execution = re.search(r'name="execution" value="([^"]+)"', response.text).group(1)

        # POST request with login data
        payload = {
            'username': self.username,
            'password': self.pwd,
            'execution': execution,
            '_eventId': 'submit'
        }
        login_response = self.session.post(self.URL_LOGIN, data=payload)

        # Check if login was successful
        if "Connexion - CAS" not in login_response.text:
            print("Login successful")
            print
            return True
        else:
            print("Login failed")
            return False
    
    def getAbsencesPage(self):
        print("Get absences page...")
        response = self.session.get(self.URL_ABSENCES)
        return response.text
    
    def getAbsences(self):
        page = self.getAbsencesPage()
        soup = BeautifulSoup(page, 'html.parser')
        
        absences_table = soup.find_all('tr', class_='ui-widget-content')
        print("Found " + str(len(absences_table)) + " absences")
        
        absences = []
        for row in absences_table:
            columns = row.find_all('td', class_='ui-panelgrid-cell')
            absence_data = [column.get_text(strip=True) for column in columns]
            absences.append(absence_data)
            
        return absences
