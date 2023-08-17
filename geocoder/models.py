from django.db import models


class GeocodeData(models.Model):
    address = models.CharField(
        'адрес',
        max_length=100,
        unique=True
    )
    lat = models.FloatField(
        'широта'
    )
    lon = models.FloatField(
        'долгота'
    )
    geocode_date = models.DateTimeField(
        'дата запроса к геокодеру',
        auto_now=True
    )

    class Meta:
        verbose_name = 'Данные геолокации'
        verbose_name_plural = 'Данные геолокации'
        unique_together = [
            ['address']
        ]

    def __str__(self):
        return self.address
