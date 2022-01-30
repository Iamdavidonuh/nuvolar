from django.test import TestCase
from rest_framework.test import APIClient
from django.utils import timezone
from datetime import timedelta
from fleet.models import Aircraft, Airport, Flight


class TestBase(TestCase):
    """contains helper functions for all test cases"""

    api_client = APIClient()

    @staticmethod
    def _create_airport(icao_code=None):
        return Airport.objects.create(icao_code=icao_code or "GCLA")

    @staticmethod
    def _create_aircraft(serial_number=None, manufacturer=None):
        return Aircraft.objects.create(
            serial_number=serial_number or "737G62",
            manufacturer=manufacturer or "Boeing",
        )

    def _get_or_create_aircraft(self):
        aircraft = Aircraft.objects.first()
        if not aircraft:
            return self._create_aircraft()
        return aircraft

    def _get_or_create_airport(self):
        airport = Airport.objects.first()
        if not airport:
            return self._create_airport()
        return airport

    def _sample_flight_payload(self, **kwargs):
        arrival = self._get_or_create_airport()
        departure = self._get_or_create_airport()

        aircraft = self._get_or_create_aircraft()
        payload = dict(
            arrival_airport=arrival,
            arrival_date=timezone.now() + timedelta(1),
            departure_airport=departure,
            departure_date=timezone.now() + timedelta(minutes=30),
            aircraft=aircraft,
        )
        payload.update(**kwargs)
        return payload

    def _create_flight(self):
        payload = self._sample_flight_payload()

        return Flight.objects.create(**payload)
