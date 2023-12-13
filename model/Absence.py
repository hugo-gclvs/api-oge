import re

class Absence():
	def __init__(self, subject, subjectType, classroom, teacher, date, justification):
		self.subject = subject
		self.subjectType = subjectType
		self.classroom = classroom
		self.teacher = teacher
		self.date = date
		self.justification = justification

	def __str__(self):
		return "Absence: " + self.subject + " - " + self.subjectType + " - " + self.classroom + " - " + self.teacher + " - " + self.date + " - " + self.justification

