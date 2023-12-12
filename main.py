from services.api import *
from getpass import getpass

def main():
    api = OgeAPI()
    api.login()
    
    semester = int(input("Semester: "))
    absences = api.getAbsences(semester)

if __name__ == "__main__":
    main()
