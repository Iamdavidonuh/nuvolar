from rest_framework import viewsets, status
from rest_framework.response import Response
from fleet.models import Aircraft, Airport, Flight
from fleet.serializers import AirportSerializer, AircraftSerializer, FlightSerializer
from fleet.utils import compute_average, update_departure_data

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
    filterset_fields = ["departure_airport", "arrival_airport"]

    def get_queryset(self):
        # overide original queryset to add filter by departure timerange
        queryset = super().get_queryset()

        start = self.request.query_params.get("start")
        end = self.request.query_params.get("end")

        if not start or not end:
            return queryset
        return queryset.filter(departure_date__time__range=[start, end])


class ReportViewset(viewsets.ReadOnlyModelViewSet):

    queryset = Flight.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        arrival_date = self.request.query_params.get("arrival_date")
        departure_date = self.request.query_params.get("departure_date")

        if departure_date:
            queryset = queryset.filter(departure_date__gte=departure_date)
        if arrival_date:
            queryset = queryset.filter(arrival_date__lte=arrival_date)

        return queryset

    def list(self, *args, **kwargs):
        aircraft_data = {}
        queryset = self.get_queryset().order_by("id")
        for flight in queryset:
            inflight_time = (
                flight.arrival_date - flight.departure_date
            ).total_seconds() / 60

            if flight.departure_airport.icao_code not in aircraft_data.keys():
                departure_data = {
                    "flights": 1,
                    "aircrafts": {},
                }
                departure_data = update_departure_data(
                    inflight_time, flight, departure_data
                )
                aircraft_data[flight.departure_airport.icao_code] = departure_data
            else:
                aircraft_data[flight.departure_airport.icao_code]["flights"] += 1
            # compute average
            aircraft_data = compute_average(flight, aircraft_data)
        return Response(aircraft_data, status=status.HTTP_200_OK)
