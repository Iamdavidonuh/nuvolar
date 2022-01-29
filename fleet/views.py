from rest_framework import viewsets
from rest_framework.response import Response
from fleet.models import Aircraft, Airport, Flight
from fleet.serializers import AirportSerializer, AircraftSerializer, FlightSerializer

# Create your views here.


class AirportViewset(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer



class AircraftViewset(viewsets.ModelViewSet):

    queryset = Aircraft.objects.all()
    serializer_class = AircraftSerializer


class FlightViewset(viewsets.ModelViewSet):

    queryset = Flight.objects.all()
    serializer_class = FlightSerializer