from django.test import TestCase
from rest_framework.test import APIClient
from django.utils import timezone
from datetime import timedelta
from fleet.models import Aircraft, Airport, Flight


class TestBase(TestCase):
    """ contains helper functions for all test cases """

    api_client = APIClient()

    @staticmethod
    def _create_airport(icao_code=None):
        return Airport.objects.create(icao_code=icao_code or "GCLA")
    
    @staticmethod
    def _create_aircraft(serial_number=None, manufacturer=None):
        return Aircraft.objects.create(
            serial_number=serial_number or "737G62",
            manufacturer=manufacturer or "Boeing"
        )

    def _create_flight(self):
        arrival = self._create_airport(icao_code="OMAA")
        departure = self._create_airport()
        return Flight.objects.create(
            arrival_airport=arrival,
            arrival_date = timezone.now() + timedelta(1),
            departure_airport = departure,
            departure_date= timezone.now()
        )

