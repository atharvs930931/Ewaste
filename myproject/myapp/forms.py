from django import forms
from .models import EWaste
from datetime import date


class EWasteForm(forms.ModelForm):

    class Meta:
        model = EWaste
        fields = [
            'category',
            'condition',
            'weight',
            'photo',
            'location',
            'pickup_date',
            'pickup_time_slot'
        ]

        widgets = {
            'pickup_date': forms.DateInput(attrs={'type': 'date'}),
        }

    # ✅ Past date block
    def clean_pickup_date(self):
        pickup_date = self.cleaned_data.get('pickup_date')

        if pickup_date and pickup_date < date.today():
            raise forms.ValidationError("Past date not allowed.")

        return pickup_date