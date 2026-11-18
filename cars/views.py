from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CarForm, CarFilterForm
from .models import Car,CarImage , Favorite
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
# Create your views here.
@login_required
def add_car(request):

    if request.method == 'POST':

        form = CarForm(request.POST)

        images = request.FILES.getlist('images')

        if len(images) != 3:

            messages.error(request, 'You must upload exactly 3 photos.')

        elif any(
            not image.name.lower().endswith(('.png', '.jpg', '.jpeg'))
            for image in images
        ):

            messages.error(request, 'Only PNG, JPG and JPEG images are allowed.')

        elif form.is_valid():

            car = form.save(commit=False)

            car.owner = request.user

            car.save()

            for image in images:

                CarImage.objects.create(
                    car=car,
                    image=image
                )

            messages.success(request, 'Your car was successfully added!')

            return redirect('home')

    else:

        form = CarForm()

    return render(
        request,
        'cars/add_car.html',
        {'form': form}
    )


def car_detail(request, car_id):

    car = get_object_or_404(
        Car,
        id=car_id
    )

    is_favorite = False

    if request.user.is_authenticated:

        is_favorite = Favorite.objects.filter(
            user=request.user,
            car=car
        ).exists()

    return render(
        request,
        'cars/car_detail.html',
        {
            'car': car,
            'is_favorite': is_favorite,
        }
    )

def car_list(request):

    cars = Car.objects.all().order_by('-created_at')

    form = CarFilterForm(request.GET or None)

    if form.is_valid():

        city = form.cleaned_data['city']
        min_year = form.cleaned_data['min_year']
        max_year = form.cleaned_data['max_year']
        capacity = form.cleaned_data['capacity']

        if city:
            cars = cars.filter(city=city)

        if min_year:
            cars = cars.filter(year__gte=min_year)

        if max_year:
            cars = cars.filter(year__lte=max_year)

        if capacity:
            cars = cars.filter(capacity=capacity)

    paginator = Paginator(cars, 6)

    page_number = request.GET.get('page')

    cars = paginator.get_page(page_number)
    page_numbers = range(
    max(1, cars.number - 3),
    min(cars.paginator.num_pages, cars.number + 3) + 1
    )

    return render(
        request,
        'cars/car_list.html',
        {
            'cars': cars,
            'form': form,
            'page_numbers': page_numbers,
        }
    )


@login_required
@require_POST
def toggle_favorite(request, car_id):

    car = get_object_or_404(
        Car,
        id=car_id
    )

    favorite = Favorite.objects.filter(
        user=request.user,
        car=car
    )

    if favorite.exists():

        favorite.delete()

        messages.success(
            request,
            'Car removed from your favorites.'
        )

    else:

        Favorite.objects.create(
            user=request.user,
            car=car
        )

        messages.success(
            request,
            'Car added to your favorites.'
        )

    return redirect('car_detail', car_id=car.id)

@login_required
def edit_car(request, car_id):

    car = get_object_or_404(
        Car,
        id=car_id,
        owner=request.user
    )

    if request.method == 'POST':

        form = CarForm(
            request.POST,
            instance=car
        )

        uploaded_images = request.FILES.getlist('images')

        if uploaded_images and len(uploaded_images) != 3:
            messages.error(
                request,
                'Please upload exactly 3 replacement photos.'
            )

        elif uploaded_images and any(
            image.name.split('.')[-1].lower()
            not in ['png', 'jpg', 'jpeg']
            for image in uploaded_images
        ):
            messages.error(
                request,
                'Only PNG, JPG and JPEG images are allowed.'
            )

        elif form.is_valid():

            form.save()

            if uploaded_images:

                for car_image in car.images.all():
                    car_image.image.delete(save=False)
                    car_image.delete()

                for image in uploaded_images:
                    CarImage.objects.create(
                        car=car,
                        image=image
                    )

            messages.success(
                request,
                'Car listing updated successfully!'
            )

            return redirect('profile')

    else:
        form = CarForm(instance=car)

    return render(
        request,
        'cars/edit_car.html',
        {'form': form, 'car': car}
    )

@login_required
@require_POST
def delete_car(request, car_id):

    car = get_object_or_404(
        Car,
        id=car_id,
        owner=request.user
    )

    if car.rentals.exists():

        messages.error(
            request,
            'This car cannot be deleted because it has rental history.'
        )

    else:

        car.delete()

        messages.success(
            request,
            'Car listing deleted successfully!'
        )

    return redirect('profile')