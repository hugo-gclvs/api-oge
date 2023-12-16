from services.OgeAPI import *

def main():
    api = OgeAPI()
    api.login()
    
    absences = api.getAllAbsences()

    for absence in absences:
        print(absence.__str__())

if __name__ == "__main__":
    main()
