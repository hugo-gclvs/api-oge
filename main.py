from services.OgeAPI import *

def main():
    api = OgeAPI()
    api.login()
    
    semester = int(input("Semester: "))
    absences = api.getAbsences(semester)

    print(absences)

if __name__ == "__main__":
    main()
