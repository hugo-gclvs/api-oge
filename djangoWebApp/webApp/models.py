from django.db import models
from datetime import datetime
import time

class Absence():
	def __init__(self, subject, subjectType, classroom, teacher, start_date, end_date, justification):
		self.subject = subject
		self.subjectType = subjectType
		self.classroom = classroom
		self.teacher = teacher
		self.start_date = datetime.fromtimestamp(start_date)
		self.end_date = datetime.fromtimestamp(end_date)
		self.justification = justification

	def __str__(self):
		return self.subject + " - " + self.subjectType + " - " + self.classroom + " - " + self.teacher + " - " + str(self.start_date) + " - " + str(self.end_date) + " - " + self.justification


class AbsenceProcessor:
    def __init__(self, data):
        self.data = data

    def process_all(self):
        absences = []
        for entry in self.data:
            if entry:
                parser = self._determine_parser(entry[0])
                if parser:
                    absences.append(parser(entry))
        return absences

    def _determine_parser(self, entry):
        if "ITC" in entry or "MDD" in entry:
            return self._parse_itc_format
        elif "CM" in entry or "TD" in entry or "TP" in entry or "Projets" in entry:
            return self._parse_standard_format
        # Add more conditions for different formats
        return None

    def _parse_standard_format(self, entry):
        subject_details, classroom_info = entry[0].split(' \n ')
        subject_parts = subject_details.split()

        # Initialize subject_type_index with a default value
        subject_type_index = -1

        # Find the index where CM, TD, or TP appears
        for i, part in enumerate(subject_parts):
            if part in ["CM", "TD", "TP", "Projets"]:
                subject_type_index = i
                break

        # Handle the case where the subject type is not found
        if subject_type_index == -1:
            # You can decide how to handle this case. For example:
            subject = subject_details  # Use the entire string or set a default value
            subject_type = "Unknown"
        else:
            subject = ' '.join(subject_parts[:subject_type_index])
            subject_type = subject_parts[subject_type_index]

        classroom = classroom_info.split(' (')[0]

        return self._create_absence_object(entry, subject, subject_type, classroom)

    def _parse_itc_format(self, entry):
        # Extracting the subject and classroom from the entry
        subject_details = entry[0].split(' \n ')
        subject_parts = subject_details[0].split('_')
        subject_name = ' '.join(subject_parts[:2])  # Assuming 'ITC316_TP2_ElecNum' format
        subject_type = subject_parts[2]  # Assuming the third part is the subject type

        # Extracting the classroom info
        classroom = subject_details[1].split(' (')[0]

        return self._create_absence_object(entry, subject_name, subject_type, classroom)

    def _create_absence_object(self, entry, subject, subjectType, classroom):
        teacher = entry[1]
        start_date, end_date = self.convert_to_timestamps(entry[2])
        justification = entry[3] if len(entry) > 3 else "Justifié"
        return Absence(subject, subjectType, classroom, teacher, start_date, end_date, justification)
    
    def convert_to_timestamps(self, date_str):
        date_part, times_part = date_str.replace("Le ", "").split(' de ')
        start_time_str, end_time_str = times_part.split(' à ')

        # Combining date and start time, and converting to a timestamp
        start_datetime_str = f"{date_part} {start_time_str}"
        start_dt_obj = datetime.strptime(start_datetime_str, "%d/%m/%Y %H:%M")
        start_timestamp = int(time.mktime(start_dt_obj.timetuple()))

        # Combining date and end time, and converting to a timestamp
        end_datetime_str = f"{date_part} {end_time_str}"
        end_dt_obj = datetime.strptime(end_datetime_str, "%d/%m/%Y %H:%M")
        end_timestamp = int(time.mktime(end_dt_obj.timetuple()))

        return start_timestamp, end_timestamp