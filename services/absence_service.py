import logging

from bs4 import BeautifulSoup
import utils.data_processing as data_processing


class AbsenceService:
    def __init__(self, oge_scraper):
        self.oge_scraper = oge_scraper

    def getAbsencesByPeriod(self, timestamp_start, timestamp_end):
        """
        This method is used to get the absences from the OGE.

        Parameters:
            timestamp_start (int): The start of the period.
            timestamp_end (int): The end of the period.

        Returns:
            list: The absences.
        """
        semesters = self._countSemesters()

        absences = []
        for semester in range(semesters, 0, -1):
            absencesPage = self._fetchAbsencesForSemester(semester)
            if absencesPage:
                absences += data_processing.create_absences(absencesPage)

        filtered_absences = filter(lambda absence: absence.start_date.timestamp() >= timestamp_start and absence.end_date.timestamp() <= timestamp_end, absences)

        return filtered_absences

    def getAbsencesByTeacher(self, teacher):
        """
        This method is used to get the absences from the OGE.

        Parameters:
            teacher (str): The teacher to get the absences from.

        Returns:
            list: The absences.
        """
        semesters = self._countSemesters()

        absences = []
        for semester in range(semesters, 0, -1):
            absencesPage = self._fetchAbsencesForSemester(semester)
            if absencesPage:
                absences += data_processing.create_absences(absencesPage)

        filtered_absences = filter(lambda absence: absence.teacher == teacher, absences)

        return filtered_absences

    def getAbsencesBySemester(self, semester):
        """
        This method is used to get the absences from the OGE.

        Parameters:
            semester (int): The semester to get the absences from.

        Returns:
            list: The absences.
        """
        absencesPage = self._fetchAbsencesForSemester(semester)
        if absencesPage:
            return data_processing.create_absences(absencesPage)
        else:
            return []

    def getAllAbsencesByClassroom(self, classroom):
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

        filtered_absences = filter(lambda absence: absence.classroom == classroom, absences)

        return filtered_absences
        
    def getAllAbsencesBySubjectType(self, subjectType):
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

        filtered_absences = filter(lambda absence: absence.subjectType == subjectType, absences)

        return filtered_absences

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
            absencesPage = self.oge_scraper.getAbsencesPage()
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
            absencesPage = self.oge_scraper.getAbsencesPage()
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
            return self.oge_scraper.postAbsencesForSemester(semester)
        except Exception as e:
            logging.error(f"Error in selecting absences semester: {e}")
            return None
    