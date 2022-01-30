from rest_framework import serializers
from datetime import date
from django.utils.translation import gettext_lazy as _
from fleet.models import Aircraft, Airport, Flight

class AircraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = Aircraft
        fields = "__all__"

class AirportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Airport
        fields = "__all__"



class FlightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flight
        fields = "__all__"

    def validate(self, data):

        if data['departure_date'] < date.today():
            raise serializers.ValidationError({"departure_date": _("A flight can only be created for a future departure")})

        if data['arrival_date'] < data['departure_date'] or data['arrival_date'] < date.today():
            raise serializers.ValidationError({"arrival_date": _("arrival date can not be in the past")})

        return data

