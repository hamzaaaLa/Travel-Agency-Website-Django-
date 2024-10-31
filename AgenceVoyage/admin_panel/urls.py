from django.urls import path
from . import views
from .views import logout_view



urlpatterns = [
    path('get_avions_by_destination/', views.get_avion_and_hotel_by_destination, name='get_avion_and_hotel_by_destination'),
    path('get_avions_and_hotels/', views.get_avions_and_hotels, name='get_avions_and_hotels'),
    path('get_countries_by_category/', views.get_countries_by_category, name='get_countries_by_category'),
    path('get_destinations_by_country/', views.get_destinations_by_country, name='get_destinations_by_country'),
    path('get_countries/', views.get_countries, name='get_countries'),
    path('get_countriesDest/', views.get_countriesDestination, name='get_countriesDest'),
    #path('example/', views.example_view, name='example'),
    # Ajoutez d'autres modèles d'URL au besoin
    path('adminHome/',views.home,name='adminHome'),
    path('adminHome/gestionVoyage',views.gestionVoyage,name='gestionVoyage'),
    path('adminHome/gestionAvion',views.gestionAvion,name='gestionAvion'),
    path('adminHome/gestionHotel',views.gestionHotel,name='gestionHotel'),
    path('adminHome/gestionClient',views.gestionClient,name='gestionClient'),
    path('adminHome/gestionCategorie',views.gestionCategorie,name='gestionCategorie'),
    path('adminHome/gestionCategorie/ajoutCategorie',views.ajoutCategorie,name='ajoutCategorie'),
    path('adminHome/gestionCategorie/editCategorie/<int:pk>/', views.editCategorie, name='editCategorie'),
    path('adminHome/gestionCategorie/deleteCategorie/<int:pk>/', views.deleteCategorie, name='deleteCategorie'),
    path('adminHome/gestionVille/deleteDes/<int:pk>/', views.deleteDes, name='deleteDes'),
    path('adminHome/gestionCountrie',views.gestionCountrie,name='gestionCountrie'),
    path('adminHome/gestionCategorie/ajoutCountry',views.ajoutCountry,name='ajoutCountry'),
    path('adminHome/gestionCountry/editCountry/<int:pk>/', views.editCountry, name='editCountry'),
    path('adminHome/gestionCountry/deleteCountry/<int:pk>/', views.deleteCountry, name='deleteCountry'),

    path('adminHome/gestionVille',views.gestionVille,name='gestionVille'),
    path('adminHome/gestionVille/ajoutDestination',views.ajoutDestination,name='ajoutDestination'),
    path('adminHome/gestionVille/editDestination/<int:pk>/',views.editDestination,name='editDestination'),
    path('adminHome/gestionVille/editDestinationForm/<int:pk>/', views.editDestinationForm, name='editDestinationForm'),


    path('adminHome/gestionVoyage/ajoutVoyage',views.ajoutVoyage,name='ajoutVoyage'),
    path('adminHome/gestionVoyage/editVoyage/<int:pk>/', views.editVoyage, name='editVoyage'),
    path('adminHome/gestionVoyage/deleteVoyage/<int:pk>/', views.deleteVoyage, name='deleteVoyage'),
    path('adminHome/gestionAvion/ajoutAvion',views.ajoutAvion,name='ajoutAvion'),
    path('adminHome/gestionAvion/editAvion/<int:pk>/', views.editAvion, name='editAvion'),
    path('adminHome/gestionAvion/deleteAvion/<int:pk>/', views.deleteAvion, name='deleteAvion'),
    path('adminHome/gestionHotel/ajoutHotel',views.ajoutHotel,name='ajoutHotel'),
    path('adminHome/gestionHotel/editHotel/<int:pk>/', views.editHotel, name='editHotel'),
    path('adminHome/gestionHotel/deleteHotel/<int:pk>/', views.deleteHotel, name='deleteHotel'),
    path('adminHome/gestionCategorie/ajoutCategorie',views.ajoutVoyage,name='ajoutCategorie'),
    path('adminHome/gestionClient/ajoutClient',views.ajoutClient,name='ajoutClient'),
    path('adminHome/gestionClient/editClient/<int:pk>/', views.editClient, name='editClient'),
    path('adminHome/gestionClient/deleteClient/<int:pk>/', views.deleteClient, name='deleteClient'),

    path('adminHome/gestionVoyage/addPromotion', views.addPromotion, name='addPromotion'),
    path('adminHome/gestionPromotion', views.gestionPromotion, name='gestionPromotion'),
    path('adminHome/gestionPromotion/deletePromotion/<int:pk>/', views.deletePromotion, name='deletePromotion'),

    path('adminHome/profile', views.profile, name='profileAdmin'),

    path('adminHome/profile/editProfile', views.editProfileView, name='editProfileAdmin'),

    path('adminHome/profile/editProfile/saveProfileChange', views.saveProfileChange, name='saveProfileChangeAdmin'),
    path('adminHome/Reservation',views.GReservation,name='GReservation'),


    path('ajoutCompte/', views.view, name='view'),
    path('ajoutCompte/ajout', views.ajoutVisa, name='ajoutVisa'),
    # Other URL patterns
    path('logout/', views.logout_view, name='logout'),
    
    
]
