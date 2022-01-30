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
    filterset_fields = ['departure_airport', 'arrival_airport']

    def get_queryset(self):
        # overide original queryset to add filter by departure timerange
        queryset = super().get_queryset()

        start = self.request.query_params.get('start')
        end = self.request.query_params.get('end')

        if not start or not end:
            return queryset
        return queryset.filter(departure_time__range=[start, end])