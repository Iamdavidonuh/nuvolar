from datetime import timedelta
from django.utils import timezone
from django.db.utils import IntegrityError
from fleet.tests import TestBase
from fleet.models import Aircraft, Airport, Flight
# Create your tests here.

class TestModels(TestBase):

    def test_airport_gets_created(self):
        airport = Airport.objects.create(icao_code="GCLA")
        fetched_airport = Airport.objects.get(id = airport.id)
        self.assertIsNotNone(fetched_airport)
        
    def test_create_aircraft_succeeds(self):

        aircraft = Aircraft.objects.create(
            serial_number = "129GC4",
            manufacturer = "Greatness"
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
            arrival_airport=arrival,
            arrival_date = timezone.now() + timedelta(1),
            departure_airport = departure,
            departure_date= timezone.now()
        )
        fetched_flight = Flight.objects.get(id=flight.id)
        self.assertIsNotNone(fetched_flight)    


