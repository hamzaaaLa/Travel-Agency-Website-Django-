from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Users(AbstractUser):
    id=models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    is_admin = models.BooleanField(default=False)
    groups = models.ManyToManyField('auth.Group', related_name='customuser_groups')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='customuser_user_permissions')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, default='')
    adresse = models.CharField(max_length=800, default='')
    photo = models.ImageField(upload_to='media/', blank=True, null=True)
    