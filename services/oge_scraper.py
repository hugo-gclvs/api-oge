class OgeScraper:
    def __init__(self, session_manager):
        self.session_manager = session_manager
        
        # Initialisation des URLs
        self.initialize_urls()
        
    def initialize_urls(self):
        """
        This method is used to initialize the URLs of the OGE.

        Parameters:
        None

        Returns:
        None
        """
        self.home_url = "https://oge.polytechnique.fr/ogesip/"
        self.login_url = "https://oge.polytechnique.fr/ogesip/login.jsp"
        self.absences_url = "https://oge.polytechnique.fr/ogesip/absences.jsp"
        self.grades_url = "https://oge.polytechnique.fr/ogesip/notes.jsp"
            

    def get(self, url):
        """
        This method is used to send a GET request to the OGE.
        
        Parameters:
            url (str): The URL of the request.
            
        Returns:
            requests.Response: The response of the request.
        """
        print(f"Get {url}")
        return self.session.get(url)

    def getAbsencesPage(self):
        """
        This method is used to get the absences page from the OGE.

        Parameters:
            None

        Returns:
            str: The absences page.
        """
        print("Get absences page...")
        response = self.session.get(self.absences_url)
        return response.text
    
    def getGradesPage(self):
        """
        This method is used to get the grades page from the OGE.

        Parameters:
            None
            
        Returns:
            str: The grades page.
        """
        print("Get grades page...")
        response = self.session.get(self.grades_url)
        return response.text
    
    def _get_headers(self):
        """
        This method is used to get the headers for the request.

        Parameters:
            None

        Returns:
            dict: The headers.
        """
        return {
            "Faces-Request": "partial/ajax",
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }

    def _extract_content(self, response):
        """
        This method is used to extract the content from the response.

        Parameters:
            response (requests.Response): The response to process.

        Returns:
            str: The content.
        """
        content = response.text.split("![CDATA[")[1].split("]]")[0]
        return content