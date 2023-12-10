from api import *
from getpass import getpass

def main():
    api = API()
    api.login()
    
    semester = int(input("Semester: "))
    absences = api.getAbsences(semester)
    print(absences)

if __name__ == "__main__":
    main()
