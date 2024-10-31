from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Categorie(models.Model):
    id = models.AutoField(primary_key=True)
    nom=models.CharField(max_length=200,unique=True)
    photo = models.ImageField(upload_to='media/', blank=True, null=True)

class Country(models.Model):
    id = models.AutoField(primary_key=True)
    categorie=models.ForeignKey(Categorie, on_delete=models.CASCADE)
    nom=models.CharField(max_length=200)
    photo = models.ImageField(upload_to='media/', blank=True, null=True)

class Destination(models.Model):
    id = models.AutoField(primary_key=True)
    country=models.ForeignKey(Country, on_delete=models.CASCADE)
    nom=models.CharField(max_length=200)
    photo = models.ImageField(upload_to='media/', blank=True, null=True)

class Voyage(models.Model):
    id = models.AutoField(primary_key=True)
    destination=models.ForeignKey(Destination, on_delete=models.CASCADE)
    duration=models.IntegerField()
    price= models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField()
    photo = models.ImageField(upload_to='media/', blank=True, null=True)

class Avion(models.Model):
    id = models.AutoField(primary_key=True)
    avionNom=models.CharField(max_length=200)
    dateDepart=models.DateField()
    dateRetour=models.DateField()
    countryDepart=models.CharField(max_length=200)
    villeDepart=models.CharField(max_length=200)
    classe=models.CharField(max_length=10)
    voyage=models.ForeignKey(Voyage, on_delete=models.CASCADE)
    countryDestination=models.CharField(max_length=200)
    villeDestination=models.CharField(max_length=200)

class Hotel(models.Model):
    id = models.AutoField(primary_key=True)
    hotelNom=models.CharField(max_length=200)
    country=models.CharField(max_length=200)
    ville=models.CharField(max_length=200)
    voyage=models.ForeignKey(Voyage, on_delete=models.CASCADE)