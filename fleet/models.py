from django.db import models

# Create your models here.


class Airport(models.Model):
    icao_code = models.CharField(max_length=4, unique=True)

    def __str__(self) -> str:
        return f"{self.icao_code}"


class Aircraft(models.Model):
    serial_number = models.CharField(max_length=15, unique=True)
    manufacturer = models.CharField(max_length=25)

    def __str__(self) -> str:
        return f"{self.serial_number} - {self.manufacturer}"

class Flight(models.Model):
    
    arrival_airport = models.ForeignKey(Airport, on_delete=models.DO_NOTHING, related_name='arrival')
    arrival_date = models.DateTimeField()

    departure_airport = models.ForeignKey(Airport, on_delete=models.DO_NOTHING, related_name='departure')
    departure_date = models.DateTimeField()
    
    aircraft = models.ForeignKey(Aircraft, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self) -> str:
        return f"Flight {self.id} From {self.departure_airport} To {self.arrival_airport}"
