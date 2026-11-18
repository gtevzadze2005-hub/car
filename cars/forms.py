from django import forms
from .models import Car


class CarForm(forms.ModelForm):

    class Meta:
        model = Car

        fields = [
            'brand',
            'model',
            'year',
            'daily_price',
            'capacity',
            'transmission',
            'city',
            'fuel_tank_capacity',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({
                    'class': 'form-select'
                })

            else:
                field.widget.attrs.update({
                    'class': 'form-control'
                })

class CarFilterForm(forms.Form):

    city = forms.ChoiceField(
        required=False,
        choices=[],
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    min_year = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Minimum year'
        })
    )

    max_year = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Maximum year'
        })
    )

    capacity = forms.IntegerField(
        required=False,
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Passengers'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        cities = Car.objects.order_by(
            'city'
        ).values_list(
            'city',
            flat=True
        ).distinct()

        self.fields['city'].choices = [
            ('', 'All cities')
        ] + [
            (city, city) for city in cities
        ]

    def clean(self):

        cleaned_data = super().clean()

        min_year = cleaned_data.get('min_year')
        max_year = cleaned_data.get('max_year')

        if min_year and max_year and min_year > max_year:
            raise forms.ValidationError(
                'Minimum year cannot be greater than maximum year.'
            )

        return cleaned_data