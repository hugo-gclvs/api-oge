from django.urls import path
from . import views

app_name = 'absences'
urlpatterns = [
	path('', views.home_page, name='home_page'),
	path('get_all_absences/', views.get_all_absences, name='get_all_absences'),
	path('get_all_teachers/', views.get_all_teachers, name='get_all_teachers'),
	path('get_all_classrooms/', views.get_all_classrooms, name='get_all_classrooms'),
]