from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User

from services.session_manager import SessionManager

class MyCustomBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        print(username)
        print(password)
        session_manager = SessionManager(user=username, pwd=password)
        if session_manager.login():
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # Créez un nouvel utilisateur
                user = User(username=username)
                user.set_unusable_password()
                user.save()
            return user
        return None
