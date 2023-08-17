from django.contrib import admin

from .models import GeocodeData


@admin.register(GeocodeData)
class GeocodeDataAdmin(admin.ModelAdmin):
    list_display = (
        'address',
        'lat',
        'lon',
        'geocode_date'
    )
