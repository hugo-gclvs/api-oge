from services.OgeAPI import *

def main():
    api = OgeAPI()
    api.login()
    
    absences = api.getAllAbsences()

    print(absences)

if __name__ == "__main__":
    main()
