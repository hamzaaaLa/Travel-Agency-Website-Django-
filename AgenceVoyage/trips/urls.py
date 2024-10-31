from django.urls import path,include
from . import views

urlpatterns=[
     
    path('', views.home,name="home"),
    path('country/<int:pk>', views.country,name="country"),
    path('destinationDetails/<int:pk>',views.destinationDetails,name="destinationDetails"),
    path('destinationDetails/voyageBooking/<int:pk>',views.voyageBooking,name="voyageBooking"),
    path('destinationDetails/voyageBooking/reservationDetails',views.reservationDetails,name="reservationDetails"),
    path('destinationDetails/voyageBooking/reservationDetails/cancelReservation/<int:pk>',views.cancelReservation,name="cancelReservation"),
    path('destinationDetails/voyageBooking/reservationDetails/cancelReservation/infosBanque/<int:pk>',views.infosBanque,name="infosBanque"),
    path('destinationDetails/voyageBooking/reservationDetails/cancelReservation/infosBanck/reverserArgent/<int:pk>',views.reverserArgent,name="reverserArgent"),
    path('destinationDetails/voyageBooking/reservationDetails/editReservation/<int:pk>',views.editReservation,name="editReservation"),
    path('client/profile', views.profile, name='profileClient'),

    path('client/profile/editProfile', views.editProfileView, name='editProfileClient'),

    path('client/profile/editProfile/saveProfileChange', views.saveProfileChange, name='saveProfileChangeClient'),
    
    path('tripsv/', views.tripsv, name='tripsv'),
    
    
]  
 
   