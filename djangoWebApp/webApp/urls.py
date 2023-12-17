from django.urls import path
from . import views

urlpatterns = [
	path('', views.welcome_page, name='welcome_page'),
    path('get_all_absences/', views.get_all_absences, name='get_all_absences'),
]
