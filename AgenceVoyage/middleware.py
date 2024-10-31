from django.shortcuts import redirect
from django.urls import reverse


class RedirectIfNotAuthenticatedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not request.user.is_authenticated and request.path.startswith('/adminHome/'):
            return redirect(reverse('login'))  # Redirect to the login page in the 'users' app
        if request.user.is_authenticated and request.path.startswith('/adminHome/'):
            if request.user.is_admin :
                return response #home est nom de l url
            else:
                return redirect(reverse('home'))
        return response 