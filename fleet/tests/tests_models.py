from datetime import timedelta, date, time
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.utils import IntegrityError
from fleet.tests import TestBase
from fleet.models import Aircraft, Airport, Flight

# Create your tests here.


class TestModels(TestBase):
    def test_airport_gets_created(self):
        airport = Airport.objects.create(icao_code="GCLA")
        fetched_airport = Airport.objects.get(id=airport.id)
        self.assertIsNotNone(fetched_airport)

    def test_create_aircraft_succeeds(self):

        aircraft = Aircraft.objects.create(
            serial_number="129GC4", manufacturer="Greatness"
        )
        fetched_aircraft = Aircraft.objects.get(id=aircraft.id)
        self.assertIsNotNone(fetched_aircraft)

    def test_aircraft_creation_with_duplicate_serial_number_fails(self):
        self._create_aircraft(serial_number="123ABC")
        with self.assertRaises(IntegrityError):
            self._create_aircraft(serial_number="123ABC")

    def test_create_flight_succeeds(self):
        arrival = self._create_airport(icao_code="OMAA")
        departure = self._create_airport()
        flight = Flight.objects.create(
            departure_airport=departure,
            departure_date=timezone.now() + timedelta(minutes=40),
            arrival_airport=arrival,
            arrival_date=timezone.now() + timedelta(1),
        )
        fetched_flight = Flight.objects.get(id=flight.id)
        self.assertIsNotNone(fetched_flight)

    def test_create_flight_fails_with_past_departure(self):
        """Test to check if the departure datetime is older than the current datetime's date.today()"""

        arrival = self._create_airport(icao_code="OMAA")
        departure = self._create_airport()

        with self.assertRaises(ValidationError):
            Flight.objects.create(
                departure_airport=departure,
                departure_date=timezone.now() - timedelta(2),
                arrival_airport=arrival,
                arrival_date=timezone.now() + timedelta(1),
            )

    def test_flight_arrival_time_fails_if_older_than_departure_time(self):
        """Test checks if the arrival datetime is older than the departure datetime"""

        arrival = self._create_airport(icao_code="OMAA")
        departure = self._create_airport()

        with self.assertRaises(ValidationError):

            Flight.objects.create(
                departure_airport=departure,
                departure_date=timezone.now() + timedelta(minutes=20),
                arrival_airport=arrival,
                arrival_date=timezone.now() - timedelta(1),
            )
