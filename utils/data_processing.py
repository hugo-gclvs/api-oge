from bs4 import BeautifulSoup
from model.Absence import Absence

def create_absences(absencesPage):
	soup = BeautifulSoup(absencesPage, 'html.parser')

	absences_table = soup.find_all('tr', class_='ui-widget-content')
	print(f"Found {len(absences_table)} absences")

	absences_data = []
	for row in absences_table:
		columns = row.find_all('td', class_='ui-panelgrid-cell')
		absence_data = [column.get_text(strip=True) for column in columns]
		absences_data.append(absence_data)

	return absences_data