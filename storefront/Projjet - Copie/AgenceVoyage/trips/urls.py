from django.urls import path
from . import views

urlpatterns=[
    path('', views.home,name="home"),
     path('voyage/<int:pk>', views.voyage,name="voyage"),
    
]  
 
 