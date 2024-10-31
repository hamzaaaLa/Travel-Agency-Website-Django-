from django.db import models
from django.contrib.auth.models import AbstractUser
from users.models import Users
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

class Avion(models.Model):
    id=models.AutoField(primary_key=True)
    nomAvion=models.CharField(max_length=200)
    villeDepart=models.CharField(max_length=200)
    dateDepart=models.DateField()
    dateRetour=models.DateField()
    destination=models.ForeignKey(Destination, on_delete=models.CASCADE)
    prix=models.DecimalField(max_digits=18, decimal_places=2)

class Hotel(models.Model):
    id = models.AutoField(primary_key=True)
    hotelNom=models.CharField(max_length=200)
    localisation=models.ForeignKey(Destination, on_delete=models.CASCADE)
    etoile=models.CharField(max_length=20)
    prixChambreSingle=models.DecimalField(max_digits=18, decimal_places=2)
    prixChambreDouble=models.DecimalField(max_digits=18, decimal_places=2)
    prixChambreSubTriple=models.DecimalField(max_digits=18, decimal_places=2)
    prixEnfant=models.DecimalField(max_digits=18, decimal_places=2)
    prixBebe=models.DecimalField(max_digits=18, decimal_places=2)


class Voyage(models.Model):
    id = models.AutoField(primary_key=True)
    destination=models.ForeignKey(Destination, on_delete=models.CASCADE)
    avion=models.ForeignKey(Avion, on_delete=models.CASCADE)
    hotel=models.ForeignKey(Hotel, on_delete=models.CASCADE)
    duration=models.IntegerField()
    prix= models.DecimalField(max_digits=18, decimal_places=2)
    description = models.TextField()
    photo = models.ImageField(upload_to='media/', blank=True, null=True)
    nombre_places=models.IntegerField(default=0)


class CompteVisa(models.Model):
    id=models.AutoField(primary_key=True)
    nomComplet=models.CharField(max_length=200,unique=True)
    cardNumber=models.CharField(max_length=200,unique=True)
    code=models.CharField(max_length=200)
    solde=models.DecimalField(max_digits=29, decimal_places=2)
 
class ComptePayPal(models.Model):
    id=models.AutoField(primary_key=True)
    nomComplet=models.CharField(max_length=200,unique=True)
    cardNumber=models.CharField(max_length=200,unique=True)
    code=models.CharField(max_length=200)
    solde=models.DecimalField(max_digits=29, decimal_places=2)

class Reservation(models.Model):
    id=models.AutoField(primary_key=True)
    voyage=models.ForeignKey(Voyage, on_delete=models.CASCADE)
    client=models.ForeignKey(Users, on_delete=models.CASCADE)
    nbDePlace=models.IntegerField(default=0)
    nbDeChambre=models.IntegerField(default=0)
    prixTotal=models.DecimalField(max_digits=29, decimal_places=2)

class Promotion(models.Model):
    id=models.AutoField(primary_key=True)
    voyage=models.ForeignKey(Voyage, on_delete=models.CASCADE)
    pourcentagePromotion=models.DecimalField(max_digits=10, decimal_places=2)
    nouveauPrix=models.DecimalField(max_digits=29, decimal_places=2)
    dateDebut=models.DateField()
    dateFin=models.DateField()

class NotificationClient(models.Model):
    id=models.AutoField(primary_key=True)
    description=models.CharField(max_length=800, default='')
    voyage=models.CharField(max_length=800, default='')

class NotificationAdmin(models.Model):
    id=models.AutoField(primary_key=True)
    description=models.CharField(max_length=800, default='')
    voyage=models.CharField(max_length=800, default='')
    client=models.CharField(max_length=800, default='')