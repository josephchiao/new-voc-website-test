from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from ubc_voc_website.decorators import Admin, Members, Execs

from .models import Trip
from .forms import TripForm, TripSignupForm

import datetime

def trip_agenda(request):
    upcoming_trips = Trip.objects.filter(start_time__gte=datetime.datetime.now()).order_by('start_time')
    return render(request, 'trips/trip_agenda.html', {'trips': upcoming_trips})

@Members
def my_trips(request):
    # base page for all trips, can navigate to create/edit pages from here
    pass

@Members
def create_trip(request):
    if request.method == "POST":
        form = TripForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            return redirect('trips')
    else:
        form = TripForm()
    return render(request, 'trips/create.html', {'form': form})

@Members
def edit_trip(request):
    pass

@Members
def view_trip(request):
    pass
