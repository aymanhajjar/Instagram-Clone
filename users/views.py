from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import User
from home.models import profile
# Create your views here.

def userlogin (request):
    if request.method == "POST":
        
        # attempt to sign in
        usercred = request.POST["cred"]
        userpassword = request.POST["password"]

        user = authenticate(request, username = usercred, password=userpassword)

        # check if login successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            message = True
            return render (request, "login.html", {
                "message": message,
                "messagetext": "Invalid username and/or password."
            })

    return render (request, "login.html")

def userlogout (request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))
    
def register(request):
    if request.method == "POST":
    
    #get parameters
        useremail = request.POST["email"]
        username = request.POST["username"]
        userfullname = request.POST["fullname"]
        userpassword = request.POST["password"]

    #attempt to create user
        try:
            user = User.objects.create_user(username, useremail, userpassword)
            user.save()
        except IntegrityError:
            message = True
            return render (request, "register.html", {
                "message": message,
                "messagetext": "Username already taken!"
            })
    
    #if successful login user
        login(request, user)

        thisuser = User.objects.get(username=request.user.username)
        userprof = profile(owner=thisuser)
        userprof.save()
        return HttpResponseRedirect(reverse("home"))

    return render(request, "register.html")
