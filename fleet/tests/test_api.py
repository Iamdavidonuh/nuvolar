from rest_framework import status
from django.urls import reverse
from fleet.tests import TestBase

from fleet.models import Airport
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

