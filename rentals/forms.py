from django import forms
from django.utils import timezone


class RentalForm(forms.Form):

    start_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )

    end_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )

    def clean(self):

        cleaned_data = super().clean()

        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        today = timezone.localdate()

        if start_date and start_date < today:
            self.add_error(
                'start_date',
                'The rental start date cannot be in the past.'
            )

        if start_date and end_date:

            if end_date <= start_date:
                self.add_error(
                    'end_date',
                    'The end date must be after the start date.'
                )

        return cleaned_data

class PaymentForm(forms.Form):

    cardholder_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Name on card'
        })
    )

    card_number = forms.CharField(
        max_length=16,
        min_length=16,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '16 digit card number'
        })
    )

    expiry_date = forms.CharField(
        max_length=4,
        min_length=4,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'MMYY'
        })
    )

    cvv = forms.CharField(
        max_length=3,
        min_length=3,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '3 digit CVV'
        })
    )

    def clean_card_number(self):
        value = self.cleaned_data['card_number']

        if not value.isdigit():
            raise forms.ValidationError(
                'Card number must contain only digits.'
            )

        return value

    def clean_expiry_date(self):
        value = self.cleaned_data['expiry_date']

        if not value.isdigit():
            raise forms.ValidationError(
                'Expiry date must contain only digits.'
            )

        return value

    def clean_cvv(self):
        value = self.cleaned_data['cvv']

        if not value.isdigit():
            raise forms.ValidationError(
                'CVV must contain only digits.'
            )

        return value
