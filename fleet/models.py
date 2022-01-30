from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

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

    departure_airport = models.ForeignKey(
        Airport, on_delete=models.DO_NOTHING, related_name="departure"
    )
    departure_date = models.DateTimeField()

    arrival_airport = models.ForeignKey(
        Airport, on_delete=models.DO_NOTHING, related_name="arrival"
    )
    arrival_date = models.DateTimeField()

    aircraft = models.ForeignKey(
        Aircraft, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self) -> str:
        return (
            f"Flight {self.id} From {self.departure_airport} To {self.arrival_airport}"
        )

    def clean(self):
        if self.arrival_date < self.departure_date:
            raise ValidationError(
                {"arrival_date": _("arrival date can not be in the past")}
            )

        if self.departure_date < timezone.now():
            raise ValidationError(
                {
                    "departure_date": _(
                        "A flight can only be created for a future departure"
                    )
                }
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
