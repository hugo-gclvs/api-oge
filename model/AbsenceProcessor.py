import re
from model.Absence import Absence

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
        elif "CM" in entry or "TD" in entry or "TP" in entry:
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
            if part in ["CM", "TD", "TP"]:
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
        date = entry[2]
        justification = entry[3] if len(entry) > 3 else "Justifié"
        return Absence(subject, subjectType, classroom, teacher, date, justification)