from django.urls import path
from .views import *

urlpatterns = [
    path('', trip_agenda, name="trip_agenda"),
    path('create', create_trip, name="create_trip")
]