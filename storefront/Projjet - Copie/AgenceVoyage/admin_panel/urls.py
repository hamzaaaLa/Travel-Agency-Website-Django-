from django.urls import path
from . import views

urlpatterns = [
    path('get_countries_by_category/', views.get_countries_by_category, name='get_countries_by_category'),
    path('get_destinations_by_country/', views.get_destinations_by_country, name='get_destinations_by_country'),
    path('get_countries/', views.get_countries, name='get_countries'),
    path('get_countriesDest/', views.get_countriesDestination, name='get_countriesDest'),
    #path('example/', views.example_view, name='example'),
    # Ajoutez d'autres modèles d'URL au besoin
    path('adminHome/',views.home,name='adminHome'),
    path('adminHome/gestionVoyage',views.gestionVoyage,name='gestionVoyage'),

    path('adminHome/gestionCategorie',views.gestionCategorie,name='gestionCategorie'),
    path('adminHome/gestionCategorie/ajoutCategorie',views.ajoutCategorie,name='ajoutCategorie'),
    path('adminHome/gestionCategorie/editCategorie/<int:pk>/', views.editCategorie, name='editCategorie'),
    path('adminHome/gestionCategorie/deleteCategorie/<int:pk>/', views.deleteCategorie, name='deleteCategorie'),

    path('adminHome/gestionCountrie',views.gestionCountrie,name='gestionCountrie'),
    path('adminHome/gestionCategorie/ajoutCountry',views.ajoutCountry,name='ajoutCountry'),
    path('adminHome/gestionCountry/editCountry/<int:pk>/', views.editCountry, name='editCountry'),
    path('adminHome/gestionCountry/deleteCountry/<int:pk>/', views.deleteCountry, name='deleteCountry'),

    path('adminHome/gestionVille',views.gestionVille,name='gestionVille'),
    path('adminHome/gestionVille/ajoutDestination',views.ajoutDestination,name='ajoutDestination'),
    path('adminHome/gestionVille/editDestination/<int:pk>/',views.editDestination,name='editDestination'),
    path('adminHome/gestionCountry/deleteDestination/<int:pk>/', views.deleteDestination, name='deleteDestination'),

    path('adminHome/gestionVoyage/ajoutVoyage',views.ajoutVoyage,name='ajoutVoyage'),
    path('adminHome/gestionCategorie/ajoutCategorie',views.ajoutVoyage,name='ajoutCategorie'),
    
]