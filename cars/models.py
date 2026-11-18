from django.db import models
from django.conf import settings


class Car(models.Model):

    class Transmission(models.TextChoices):
        AUTOMATIC = 'automatic', 'Automatic'
        MANUAL = 'manual', 'Manual'
        TIPTRONIC = 'tiptronic', 'Tiptronic'

    brand = models.CharField(max_length=100)

    model = models.CharField(max_length=100)

    year = models.PositiveSmallIntegerField()

    daily_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    capacity = models.PositiveSmallIntegerField()

    transmission = models.CharField(
        max_length=20,
        choices=Transmission.choices
    )

    city = models.CharField(max_length=100)

    fuel_tank_capacity = models.PositiveSmallIntegerField()

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cars'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.brand} {self.model} ({self.year})'


class CarImage(models.Model):

    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = models.ImageField(upload_to='cars/')

    def __str__(self):
        return f'Image of {self.car}'


class Favorite(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorites'
    )

    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='favorited_by'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'car')

    def __str__(self):
        return f'{self.user} likes {self.car}'