from django.shortcuts import render
from cars.models import Car
# Create your views here
def home(request):

    cars = Car.objects.all().order_by('-created_at')[:6]

    random_cars = Car.objects.order_by('?')[:6]

    return render(
        request,
        'core/home.html',
        {
            'cars': cars,
            'random_cars': random_cars,
        }
    )