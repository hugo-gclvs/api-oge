from django.urls import path
from . import views

urlpatterns = [
    path('afficher/', views.afficher_donnees, name='afficher_donnees'),
    path('afficher_absences/', views.afficher_absences, name='afficher_absences'),
]
