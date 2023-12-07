from api import *
from getpass import getpass

def main():
    api = API()
    api.login()
    absences = api.getAbsences()
    print(absences)

if __name__ == "__main__":
    main()
