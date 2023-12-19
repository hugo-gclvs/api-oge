import re
import time
import requests
from bs4 import BeautifulSoup
import os
import logging
from utils import data_processing
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

class OgeAPI:
    """
    This class is used to interact with the OGE API.
    
    Attributes:
        username (str): The username used to connect to the OGE.
        password (str): The password used to connect to the OGE.
        session (requests.Session): The session used to send requests to the OGE.
        home_url (str): The URL of the OGE home page.
        login_url (str): The URL of the OGE login page.
        absences_url (str): The URL of the OGE absences page.
        grades_url (str): The URL of the OGE grades page.
    """
    def __init__(self, user=os.getenv("API_USERNAME"), pwd=os.getenv("API_PASSWORD")):
        """
        The constructor for the OgeAPI class.
        
        Parameters:
            user (str): The username used to connect to the OGE.
            pwd (str): The password used to connect to the OGE.
            
        Returns:
            None
        """
        self.username = user
        self.password = pwd
        self.session = requests.Session()
        self.initialize_urls()

    
    
    
    

    
    
    
