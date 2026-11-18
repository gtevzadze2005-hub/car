from django.shortcuts import render,  redirect
from .forms import RegisterForm , LoginForm
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST 
from cars.models import Car, Favorite
from django.contrib.auth.decorators import login_required
from rentals.models import Rental


# Create your views here.



def register(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = RegisterForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )

def user_login(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():

            phone = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']

            user = authenticate(
                request,
                phone_number=phone,
                password=password
            )

            if user is not None:
                login(request, user)
                return redirect('home')

            form.add_error(None, 'Invalid phone number or password.')

    else:
        form = LoginForm()

    return render(
        request,
        'accounts/login.html',
        {'form': form}
    )


@require_POST
def user_logout(request):

    logout(request)

    return redirect('home')


@login_required
def profile(request):

    user_cars = Car.objects.filter(
        owner=request.user
    ).order_by('-created_at')

    favorite_cars = Favorite.objects.filter(
        user=request.user
    ).select_related('car').order_by('-created_at')

    rental_history = Rental.objects.filter(
        user=request.user
    ).select_related('car').order_by('-created_at')

    incoming_rentals = Rental.objects.filter(
        car__owner=request.user
    ).select_related(
        'user',
        'car'
    ).order_by('-created_at')

    return render(
        request,
        'accounts/profile.html',
        {
            'user_cars': user_cars,
            'favorite_cars': favorite_cars,
            'rental_history': rental_history,
            'incoming_rentals': incoming_rentals,
        }
    )
