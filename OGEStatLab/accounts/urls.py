from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
	path('', views.welcome_page, name='welcome_page'),
	path('login/', views.login, name='login'),
]