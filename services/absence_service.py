import logging

from bs4 import BeautifulSoup
import utils.data_processing as data_processing


class AbsenceService:
    def __init__(self, oge_scraper):
        self.oge_scraper = oge_scraper

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
        for semester in range(semesters, 0, -1):
            absencesPage = self._fetchAbsencesForSemester(semester)
            if absencesPage:
                absences += data_processing.create_absences(absencesPage)

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