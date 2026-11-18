from django.contrib import admin
from .models import Car, CarImage
# Register your models here.
class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):

    list_display = (
        'brand',
        'model',
        'year',
        'daily_price',
        'city',
        'owner',
    )

    list_filter = (
        'city',
        'year',
        'transmission',
    )

    search_fields = (
        'brand',
        'model',
        'city',
    )

    inlines = [CarImageInline]


admin.site.register(CarImage)
