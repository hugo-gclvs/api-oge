import re

class Absence():
	def __init__(self, subject, subjectType, classroom, teacher, start_date, end_date, justification):
		self.subject = subject
		self.subjectType = subjectType
		self.classroom = classroom
		self.teacher = teacher
		self.start_date = start_date
		self.end_date = end_date
		self.justification = justification

	def __str__(self):
		return "Absence: " + self.subject + " - " + self.subjectType + " - " + self.classroom + " - " + self.teacher + " - " + str(self.start_date) + " - " + str(self.end_date) + " - " + self.justification

