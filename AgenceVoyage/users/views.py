from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Users
from django.db import IntegrityError
from admin_panel.models import NotificationAdmin

# Create your views here.
def home(request):
    return render(request,'users/index.html')
def login_user(request):
    if request.method == "POST":
        user_name = request.POST.get('UserName')
        password = request.POST.get('password')
        user = authenticate(request, username=user_name, password=password)
        if user is not None:
            login(request, user)
            if request.user.is_admin:
                return redirect("profileAdmin")
            else:
                return redirect('reservationDetails')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return render(request, 'users/login.html')
    else:
        return render(request, 'users/login.html')

def inscription(request):
        return render(request,'users/inscription.html')

def register_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        photo=request.FILES.get('photo')
        # Create a new Users object and save it to the database
        try:
            # Attempt to create a new user
            Users.objects.create(
            username=email, 
            password=password,
            first_name=first_name, 
            last_name=last_name, 
            phone=phone,
            photo=photo
            )
            NotificationAdmin.objects.create(
                description="New client is added",
                client=email
            )
            user=authenticate(request,username=email,password=password)
            login(request,user) 
            if request.user.is_admin:
                return redirect("adminHome")
            else:
                return redirect('reservationDetails')  
        except IntegrityError as e:
            # If the email already exists, render the inscription.html template with an error message
            return render(request, 'users/inscription.html', {'error_message': 'Email already exists'})
        
    else:
        return render(request,'users/inscription.html')


     
    