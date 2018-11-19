from django.shortcuts import render, HttpResponse, redirect, reverse
from django.contrib import messages
from .models import *
import bcrypt
import re


# Create your views here.
def index(request):
    try: 
        request.session['id']
        print('id is', request.session['id'])
    except KeyError as e:
        print('e', e)
        request.session['id'] = 0
        print(request.session['id'])
    return render(request,'exam/index.html')

def create(request):
    errors = User.objects.registerValidator(request.POST)

    if len(errors):
        for key, error in errors.items():
            messages.add_message(request, messages.ERROR, error, extra_tags='register')
        return redirect("/")
    else:
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(name = request.POST['name'], username = request.POST['username'], password = pw_hash)
        request.session['id'] = user.id
        return redirect('/success')

def login(request):
    errors = User.objects.loginValidator(request.POST)
    print("errors: ", errors)

    if len(errors):
        for key, error in errors.items():
            messages.add_message(request, messages.ERROR, error, extra_tags='login')
        return redirect("/")
    else:
        user = User.objects.get(username=request.POST['loguser'])
        request.session['id'] = user.id
        return redirect('/success')

def success(request):
    if request.session['id'] == 0:
        return redirect('/')
    else:
        other_trips = []
        all_trips = Trip.objects.all()
        mytrips = User.objects.get(id=request.session['id']).travel_trips.all()
        for trip in all_trips:
            if trip not in mytrips:
                other_trips.append(trip)
        context = {
            "user": User.objects.get(id=request.session['id']),
            "trips": other_trips,
            "mytrips": mytrips
            }
        return render(request,'exam/success.html', context)

def new(request):
    if request.session['id'] == 0:
        return redirect('/')
    return render(request, 'exam/newtrip.html')

def addTrip(request):
    errors = Trip.objects.tripValidator(request.POST)

    if len(errors):
        for key, error in errors.items():
            messages.add_message(request, messages.ERROR, error, extra_tags='addTrip')
        return redirect("/new")
    else:
        trip = Trip.objects.create(name = request.POST["name"], description = request.POST['description'], date_from = request.POST['date_from'], date_to = request.POST['date_to'], uploader = User.objects.get(id=request.session['id']))
        trip.travel_users.add(User.objects.get(id=request.session['id']))
        return redirect('/success')

def join(request, id):
    if request.session['id'] == 0:
        return redirect('/')
    trip = Trip.objects.get(id=id)
    trip.travel_users.add(User.objects.get(id=request.session['id']))
    return redirect('/success')

def show(request, id):
    if request.session['id'] == 0:
        return redirect('/')
    trip = Trip.objects.get(id=id)
    context = {
            "trip": trip,
            "users": trip.travel_users.all(),
            }
    return render(request, 'exam/trip.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')