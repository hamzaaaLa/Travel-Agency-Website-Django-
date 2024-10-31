from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Users(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    is_admin = models.BooleanField(default=False)
    groups = models.ManyToManyField('auth.Group', related_name='customuser_groups')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='customuser_user_permissions')
