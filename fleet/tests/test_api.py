from rest_framework import status
from django.urls import reverse
from fleet.tests import TestBase

from fleet.models import Aircraft, Airport
from fleet import serializers


class TestAirportViewsets(TestBase):

    def setUp(self) -> None:
        self.airport = self._create_airport()

    def test_create_airport_api_call_succeeds(self):
        response = self.api_client.post(reverse('airport-list'), data=dict(icao_code="TTGT"),
        format="json"
        )
        airport = Airport.objects.filter(id=response.data['id']).first()
        self.assertIsNotNone(airport)

    def test_get_all_airports(self):
        """ Test List API call """
        response = self.api_client.get(reverse("airport-list"), format="json")
        airports = Airport.objects.all()
        serializer = serializers.AirportSerializer(airports, many=True)
        self.assertEqual(response.data, serializer.data)
    
    def test_get_single_airport_succeeds(self):
        """ Tests the retrieve API call"""

        response = self.api_client.get(reverse('airport-detail', args=(self.airport.id,)))
        airport = Airport.objects.get(id=self.airport.id)
        serializer = serializers.AirportSerializer(airport)
        self.assertEqual(response.data, serializer.data)
    
    def test_get_single_airport_with_wrong_id_fails(self):
        response = self.api_client.get(reverse('airport-detail', args=(62,)))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_airport_api_call_succeeds(self):
        response = self.api_client.put(reverse('airport-detail', args=(self.airport.id,)), data=dict(
            icao_code="TTGT"
        ), format="json"
        )
        airport = Airport.objects.get(id=self.airport.id)
        self.assertEqual(response.data['icao_code'], airport.icao_code)

    def test_delete_airport_api_call_succeeds(self):
        response = self.api_client.delete(reverse('airport-detail', args=(self.airport.id,)))
        airport = Airport.objects.filter(id=self.airport.id).first()
        self.assertIsNone(airport)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestAircraftViewsets(TestBase):

    def setUp(self) -> None:
        self.aircraft = self._create_aircraft()

    def test_create_aircraft_api_call_succeeds(self):
        response = self.api_client.post(reverse('aircraft-list'), data=dict(
            serial_number="112ABC",
            manufacturer = "Big Baby"
            ),
        format="json"
        )
        aircraft = Aircraft.objects.filter(id=response.data['id']).first()
        self.assertIsNotNone(aircraft)
    
    def test_create_aircraft_with_nonunique_serial_number_fails(self):
        response = self.api_client.post(reverse('aircraft-list'), data=dict(
            serial_number=self.aircraft.serial_number,
            manufacturer = "Big Baby"
            ),
            format="json"
        )
        assert "serial number already exists" in response.data['serial_number'][0]
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_aircraft(self):
        """ Test List API call """
        response = self.api_client.get(reverse("aircraft-list"), format="json")
        aircrafts = Aircraft.objects.all()
        serializer = serializers.AircraftSerializer(aircrafts, many=True)
        self.assertEqual(response.data, serializer.data)
    
    def test_get_single_aircraft_succeeds(self):
        """ Tests the retrieve API call"""

        response = self.api_client.get(reverse('aircraft-detail', args=(self.aircraft.id,)))
        aircraft = Aircraft.objects.get(id=self.aircraft.id)
        serializer = serializers.AircraftSerializer(aircraft)
        self.assertEqual(response.data, serializer.data)
    
    def test_get_single_aircraft_with_wrong_id_fails(self):
        response = self.api_client.get(reverse('aircraft-detail', args=(62,)))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_aircraft_api_call_succeeds(self):
        response = self.api_client.put(reverse('aircraft-detail', args=(self.aircraft.id,)), data=dict(
            manufacturer="G6",
            serial_number="112ABE"
        ), format="json"
        )
        aircraft = Aircraft.objects.get(id=self.aircraft.id)
        self.assertEqual(response.data['manufacturer'], aircraft.manufacturer)

    def test_delete_aircraft_api_call_succeeds(self):
        response = self.api_client.delete(reverse('aircraft-detail', args=(self.aircraft.id,)))
        aircraft = Aircraft.objects.filter(id=self.aircraft.id).first()
        self.assertIsNone(aircraft)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

