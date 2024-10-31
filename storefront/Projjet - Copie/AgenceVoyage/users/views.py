from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
# Create your views here.
def home(request):
    return render(request,'users/index.html')

def login_user(request):
    if request.method=="POST":
        user=request.POST['UserName']
        passw=request.POST['password']
        user=authenticate(request,username=user,password=passw)
        if user is not None:
            login(request,user)
            if request.user.is_admin:
                return redirect("adminHome")#home est nom de l url
            else:
                login(request,user)
                return HttpResponse("Hello client")
        else:
            messages.success(request,("Resseyer"))
            return HttpResponse("baaka")
    else:
        return render(request,'users/login.html')