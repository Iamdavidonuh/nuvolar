from rest_framework import status
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from fleet.tests import TestBase

from fleet.models import Aircraft, Airport, Flight
from fleet import serializers


class TestAirportViewsets(TestBase):
    def setUp(self) -> None:
        self.airport = self._create_airport()

    def test_create_airport_api_call_succeeds(self):
        response = self.api_client.post(
            reverse("airport-list"), data=dict(icao_code="TTGT"), format="json"
        )
        airport = Airport.objects.filter(id=response.data["id"]).first()
        self.assertIsNotNone(airport)

    def test_get_all_airports(self):
        """Test List API call"""
        response = self.api_client.get(reverse("airport-list"), format="json")
        airports = Airport.objects.all()
        serializer = serializers.AirportSerializer(airports, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_get_single_airport_succeeds(self):
        """Tests the retrieve API call"""

        response = self.api_client.get(
            reverse("airport-detail", args=(self.airport.id,))
        )
        airport = Airport.objects.get(id=self.airport.id)
        serializer = serializers.AirportSerializer(airport)
        self.assertEqual(response.data, serializer.data)

    def test_get_single_airport_with_wrong_id_fails(self):
        response = self.api_client.get(reverse("airport-detail", args=(62,)))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_airport_api_call_succeeds(self):
        response = self.api_client.put(
            reverse("airport-detail", args=(self.airport.id,)),
            data=dict(icao_code="TTGT"),
            format="json",
        )
        airport = Airport.objects.get(id=self.airport.id)
        self.assertEqual(response.data["icao_code"], airport.icao_code)

    def test_delete_airport_api_call_succeeds(self):
        response = self.api_client.delete(
            reverse("airport-detail", args=(self.airport.id,))
        )
        airport = Airport.objects.filter(id=self.airport.id).first()
        self.assertIsNone(airport)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestAircraftViewsets(TestBase):
    def setUp(self) -> None:
        self.aircraft = self._create_aircraft()

    def test_create_aircraft_api_call_succeeds(self):
        response = self.api_client.post(
            reverse("aircraft-list"),
            data=dict(serial_number="112ABC", manufacturer="Big Baby"),
            format="json",
        )
        aircraft = Aircraft.objects.filter(id=response.data["id"]).first()
        self.assertIsNotNone(aircraft)

    def test_create_aircraft_with_nonunique_serial_number_fails(self):
        response = self.api_client.post(
            reverse("aircraft-list"),
            data=dict(
                serial_number=self.aircraft.serial_number, manufacturer="Big Baby"
            ),
            format="json",
        )
        assert "serial number already exists" in response.data["serial_number"][0]
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_aircraft(self):
        """Test List API call"""
        response = self.api_client.get(reverse("aircraft-list"), format="json")
        aircrafts = Aircraft.objects.all()
        serializer = serializers.AircraftSerializer(aircrafts, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_get_single_aircraft_succeeds(self):
        """Tests the retrieve API call"""

        response = self.api_client.get(
            reverse("aircraft-detail", args=(self.aircraft.id,))
        )
        aircraft = Aircraft.objects.get(id=self.aircraft.id)
        serializer = serializers.AircraftSerializer(aircraft)
        self.assertEqual(response.data, serializer.data)

    def test_get_single_aircraft_with_wrong_id_fails(self):
        response = self.api_client.get(reverse("aircraft-detail", args=(62,)))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_aircraft_api_call_succeeds(self):
        response = self.api_client.put(
            reverse("aircraft-detail", args=(self.aircraft.id,)),
            data=dict(manufacturer="G6", serial_number="112ABE"),
            format="json",
        )
        aircraft = Aircraft.objects.get(id=self.aircraft.id)
        self.assertEqual(response.data["manufacturer"], aircraft.manufacturer)

    def test_delete_aircraft_api_call_succeeds(self):
        response = self.api_client.delete(
            reverse("aircraft-detail", args=(self.aircraft.id,))
        )
        aircraft = Aircraft.objects.filter(id=self.aircraft.id).first()
        self.assertIsNone(aircraft)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestFlightViewsets(TestBase):
    def setUp(self) -> None:
        self.flight = self._create_flight()

    def test_create_flight_api_call_succeeds(self):
        response = self.api_client.post(
            reverse("flight-list"),
            data=dict(
                aircraft=self.flight.aircraft.id,
                departure_airport=self.flight.departure_airport.id,
                departure_date=timezone.now() + timedelta(minutes=40),
                arrival_airport=self.flight.arrival_airport.id,
                arrival_date=timezone.now() + timedelta(1),
            ),
            format="json",
        )
        flight = Flight.objects.filter(id=response.data["id"]).first()
        self.assertIsNotNone(flight)

    def test_list_all_flights_succeeds(self):
        """Test List API call"""
        response = self.api_client.get(reverse("flight-list"), format="json")
        flights = Flight.objects.all()
        serializer = serializers.FlightSerializer(flights, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_get_single_flight_succeeds(self):
        """Tests the retrieve API call"""

        response = self.api_client.get(reverse("flight-detail", args=(self.flight.id,)))
        flight = Flight.objects.get(id=self.flight.id)
        serializer = serializers.FlightSerializer(flight)
        self.assertEqual(response.data, serializer.data)

    def test_get_single_flight_with_wrong_id_fails(self):
        response = self.api_client.get(reverse("flight-detail", args=(62,)))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_flight_api_call_succeeds(self):
        response = self.api_client.delete(
            reverse("flight-detail", args=(self.flight.id,))
        )
        flight = Flight.objects.filter(id=self.flight.id).first()
        self.assertIsNone(flight)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # Negative Testing with respect to departure and arrival_dates
    def test_flight_creation_with_past_departure_date(self):
        payload = self._sample_flight_payload(
            departure_date=timezone.now() - timedelta(1)
        )
        response = self.api_client.post(reverse("flight-list"), data=payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_flight_creation_with_arrival_date_older_than_departure_date(self):
        payload = self._sample_flight_payload(
            arrival_date=timezone.now() - timedelta(1)
        )
        response = self.api_client.post(reverse("flight-list"), data=payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # tests for filters
    def test_filter_by_departure_airport(self):
        url = f"{reverse('flight-list')}?departure_airport={self.flight.departure_airport.id}"
        response = self.api_client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_by_arrival_airport(self):
        url = (
            f"{reverse('flight-list')}?arrival_airport={self.flight.arrival_airport.id}"
        )
        response = self.api_client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_by_departure_time_range(self):
        """
        Filters by departure time range using of start and end times
        """
        start_time = self.flight.departure_date.time()
        end_time = self.flight.departure_date + timedelta(hours=1)
        end_time = end_time.time()
        url = f"{reverse('flight-list')}?start={start_time}&end={end_time}"
        response = self.api_client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class TestReportViewset(TestBase):
    def setUp(self) -> None:
        self.flight_one = self._create_flight()

        flight_data = self._sample_flight_payload(
            arrival_date=timezone.now() + timedelta(days=2),
            departure_date=timezone.now() + timedelta(days=1),
        )
        self.flight_two = Flight.objects.create(**flight_data)

    def test_report_list_view(self):
        start_time = self.flight_one.departure_date.strftime("%Y-%m-%d %H:%M:%S")
        end_time = self.flight_two.arrival_date.strftime("%Y-%m-%d %H:%M:%S")
        url = f"{reverse('reports-list')}?departure_date={start_time}&arrival_date={end_time}"
        response = self.api_client.get(url, format="json")

        self.assertTrue(len(response.data), 1)
