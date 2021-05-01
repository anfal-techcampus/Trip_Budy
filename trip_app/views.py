from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.
def index(request):
    if 'user' in request.session:
        return redirect("/dashboard")
    return render(request,"index.html")

def register(request):
    errors = User.objects.validator(request.POST)
    if len(errors)>0:
        for key,val in errors.items():
            messages.error(request,val)
        return redirect("/")
    else:
        if request.method=="POST":
            password=request.POST['password']
            passHash=bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()
            User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'],
            password=passHash)
            messages.success(request,"User successfully created")
        return redirect("/dashboard")
def login(request):
    if request.method=="POST":
        user=User.objects.filter(email=request.POST['email'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user'] = logged_user.id
                messages.success(request,"Successfully logged in")
                return redirect("/dashboard")
            else:
                messages.error(request,"Email or password is not correct")
                return redirect("/")
        else:
            messages.error(request,"Email or password is not correct")
            return redirect("/")

def dashboard(request):
    if 'user' in request.session:
        # user = User.objects.get(id=request.session['user'])
        context = {
            'user' : User.objects.get(id=request.session['user']),
            'trips': Trip.objects.filter(user_in_trip=User.objects.get(id=request.session['user'])),
            'other_trips': Trip.objects.exclude(user_in_trip=User.objects.get(id=request.session['user']))
        }
        return render(request,"dashboard.html",context)
    else: 
        return redirect("/")

def new(request):
    if 'user' in request.session:
        context = {
            'user':User.objects.get(id=request.session['user'])
        }
        return render(request,"create.html",context)
    else: 
        return redirect("/")

def create(request):
    errors = Trip.objects.validator(request.POST)
    if len(errors)>0:
        for key,val in errors.items():
            messages.error(request,val)
        return redirect("/trips/new")
    else:
        if request.method=="POST":
            user = User.objects.get(id=request.session['user'])
            trip = Trip.objects.create(destination=request.POST['destination'],start_date=request.POST['start_date'],
            end_date=request.POST['end_date'],plan =request.POST['plan'],created_by= user)
            trip.user_in_trip.add(user)
            messages.success(request,"Trip successfully created")
        return redirect("/dashboard")            

def cancel(request):
        return redirect("/dashboard") 

def edit(request, id):
    if 'user' in request.session:
        context ={
        'user':User.objects.get(id=request.session['user']),
        'trip':Trip.objects.get(id=id)
        }
        # trip.user_in_trip.add(user)
        return render(request,"edit.html",context)
    else: 
        return redirect("/")

def update(request, id):
    errors = Trip.objects.validator(request.POST)
    if len(errors)>0:
        for key,val in errors.items():
            messages.error(request,val)
        return redirect(f"/trips/edit/{id}")
    else:
        if request.method=="POST":
            trip=Trip.objects.get(id=id)
            trip.destination=request.POST['destination']
            trip.start_date=request.POST['start_date']
            trip.end_date=request.POST['end_date']
            trip.plan =request.POST['plan']
            trip.save()
            messages.success(request,"Trip successfully updated")
        return redirect("/dashboard") 

def remove(request, id):
    if 'user' in request.session:
        trip = Trip.objects.get(id=id)
        trip.delete()
        return redirect("/")
    else: 
        return redirect("/")

def view(request, id):
    context = {
        'user':User.objects.get(id=request.session['user']),
        'trips':Trip.objects.get(id=id)
    }
    return render(request,"view.html",context)

def join(request, id):
    user = User.objects.get(id=request.session['user'])
    trip = Trip.objects.get(id=id)
    trip.user_in_trip.add(user)
    return redirect("/")

def notjoin(request ,id):
    user = User.objects.get(id=request.session['user'])
    trip = Trip.objects.get(id=id)
    trip.user_in_trip.remove(user)
    return redirect("/")

def logout(request):
    if 'user' in request.session:
        request.session.flush()
    return redirect("/")