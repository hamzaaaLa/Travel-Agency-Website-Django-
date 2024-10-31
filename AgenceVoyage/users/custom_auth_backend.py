# custom_auth_backend.py
from django.contrib.auth.backends import BaseBackend
from .models import Users

class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Users.objects.get(username=username)
        except Users.DoesNotExist:
            return None

        if user.password == password:
            return user
        return None

    def get_user(self, user_id):
        try:
            return Users.objects.get(pk=user_id)
        except Users.DoesNotExist:
            return None
