from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import date

from cars.models import Car
from .models import Rental , Payment
from .forms import RentalForm, PaymentForm
# Create your views here.

@login_required
def book_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if car.owner == request.user:
        messages.error(request, 'You cannot rent your own car.')
        return redirect('car_detail', car_id=car.id)

    if request.method == 'POST':
        form = RentalForm(request.POST)

        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            overlapping_rentals = Rental.objects.filter(
                car=car,
                status__in=[
                    Rental.Status.PENDING,
                    Rental.Status.CONFIRMED
                ],
                start_date__lt=end_date,
                end_date__gt=start_date
            )

            if overlapping_rentals.exists():
                form.add_error(
                    None,
                    'This car is already booked for the selected dates.'
                )
            else:
                request.session['pending_booking'] = {
                    'car_id': car.id,
                    'start_date': start_date.isoformat(),
                    'end_date': end_date.isoformat()
                }

                return redirect('payment_page')

    else:
        form = RentalForm()

    return render(request, 'rentals/book_car.html', {
        'form': form,
        'car': car
    })

@login_required
def payment_page(request):

    booking = request.session.get('pending_booking')

    if not booking:
        messages.error(request, 'No pending booking was found.')
        return redirect('car_list')

    car = get_object_or_404(Car, id=booking['car_id'])

    if car.owner == request.user:
        request.session.pop('pending_booking', None)
        messages.error(request, 'You cannot rent your own car.')
        return redirect('car_detail', car_id=car.id)

    start_date = date.fromisoformat(booking['start_date'])
    end_date = date.fromisoformat(booking['end_date'])

    rental_days = (end_date - start_date).days
    total_price = car.daily_price * rental_days

    if request.method == 'POST':
        form = PaymentForm(request.POST)

        if form.is_valid():

            card_number = form.cleaned_data['card_number'].replace(' ', '')
            expiry_date = form.cleaned_data['expiry_date']
            cvv = form.cleaned_data['cvv']

            if True:

                overlapping_rentals = Rental.objects.filter(
                    car=car,
                    status__in=[
                        Rental.Status.PENDING,
                        Rental.Status.CONFIRMED
                    ],
                    start_date__lt=end_date,
                    end_date__gt=start_date
                )

                if overlapping_rentals.exists():
                    messages.error(
                        request,
                        'Sorry, this car has just been booked for those dates.'
                    )
                    request.session.pop('pending_booking', None)
                    return redirect('car_detail', car_id=car.id)

                rental = Rental.objects.create(
                    user=request.user,
                    car=car,
                    start_date=start_date,
                    end_date=end_date,
                    total_price=total_price
                )

                Payment.objects.create(
                    rental=rental,
                    amount=total_price,
                    status=Payment.Status.SUCCESSFUL
                )

                request.session.pop('pending_booking', None)

                messages.success(
                    request,
                    'Payment successful! Your rental request has been submitted.'
                )

                return redirect('profile')

            else:
                form.add_error(
                    None,
                    'Payment failed. Please check your demo card credentials.'
                )

    else:
        form = PaymentForm()

    return render(request, 'rentals/payment.html', {
        'form': form,
        'car': car,
        'total_price': total_price,
        'rental_days': rental_days,
        'start_date': start_date,
        'end_date': end_date
    })


@login_required
@require_POST
def manage_rental(request, rental_id, action):

    rental = get_object_or_404(
        Rental,
        id=rental_id,
        car__owner=request.user
    )

    if rental.status != Rental.Status.PENDING:

        messages.error(
            request,
            'This rental request has already been processed.'
        )

    elif action == 'confirm':

        rental.status = Rental.Status.CONFIRMED
        rental.save()

        messages.success(
            request,
            'Rental request successfully confirmed.'
        )

    elif action == 'reject':

        rental.status = Rental.Status.CANCELLED
        rental.save()

        messages.success(
            request,
            'Rental request rejected.'
        )

    else:

        messages.error(
            request,
            'Invalid rental action.'
        )

    return redirect('profile')


@login_required
@require_POST
def cancel_rental(request, rental_id):

    rental = get_object_or_404(
        Rental,
        id=rental_id,
        user=request.user
    )

    if rental.status not in [
        Rental.Status.PENDING,
        Rental.Status.CONFIRMED
    ]:
        messages.error(
            request,
            'This rental cannot be cancelled.'
        )

    elif rental.start_date <= timezone.localdate():
        messages.error(
            request,
            'You cannot cancel a rental on or after its start date.'
        )

    else:
        rental.status = Rental.Status.CANCELLED
        rental.save()

        messages.success(
            request,
            'Your rental was cancelled successfully.'
        )

    return redirect('profile')


@login_required
@require_POST
def complete_rental(request, rental_id):

    rental = get_object_or_404(
        Rental,
        id=rental_id,
        car__owner=request.user
    )

    if rental.status != Rental.Status.CONFIRMED:
        messages.error(
            request,
            'Only confirmed rentals can be completed.'
        )

    elif rental.end_date > timezone.localdate():
        messages.error(
            request,
            'You cannot complete a rental before its end date.'
        )

    else:
        rental.status = Rental.Status.COMPLETED
        rental.save()

        messages.success(
            request,
            'Rental successfully marked as completed.'
        )

    return redirect('profile')
