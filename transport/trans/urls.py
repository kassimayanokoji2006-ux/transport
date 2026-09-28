from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home_name'),
    # Etudiant CRUD
    path('etudiants/', views.etudiant_list, name='etudiant_list'),
    path('etudiants/create/', views.etudiant_create, name='etudiant_create'),
    path('etudiants/<path:pk>/edit/', views.etudiant_update, name='etudiant_update'),
    path('etudiants/<path:pk>/delete/', views.etudiant_delete, name='etudiant_delete'),
    # Bus CRUD
    path('bus/', views.bus_list, name='bus_list'),
    path('bus/create/', views.bus_create, name='bus_create'),
    path('bus/<path:pk>/edit/', views.bus_update, name='bus_update'),
    path('bus/<path:pk>/delete/', views.bus_delete, name='bus_delete'),
    # Trans CRUD
    path('transports/', views.trans_list, name='trans_list'),
    path('transports/create/', views.trans_create, name='trans_create'),
    path('transports/<path:pk>/edit/', views.trans_update, name='trans_update'),
    path('transports/<path:pk>/delete/', views.trans_delete, name='trans_delete'),
]


