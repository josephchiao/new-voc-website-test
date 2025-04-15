from django import forms
from .models import GearHour, CancelledGearHour

from django.contrib.auth import get_user_model

import datetime

User = get_user_model()

class GearHourForm(forms.ModelForm):
    class Meta:
        model = GearHour
        fields = (
            'start_date',
            'end_date',
            'start_time',
            'duration'
        )

    def __init__(self, *args, gear_hour=None, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.gear_hour = gear_hour

    def save(self, commit=True):
        gear_hour = super().save(commit=False)
        if self.user:
            gear_hour.qm = self.user

        if commit:
            gear_hour.save()

        return gear_hour

    start_date = forms.DateField(
        required=True,
        initial=datetime.datetime.today(),
        widget=forms.TextInput(attrs={'class': 'flatpickr-date'})
    )
    end_date = forms.DateField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'flatpickr-date'})
    )
    start_time = forms.TimeField(
        required=True,
        initial=datetime.datetime.now().strftime('%I:%M %p'),
        input_formats=['%I:%M %p'],
        widget=forms.TextInput(attrs={'class': 'flatpickr-timeonly'})
    )
    duration = forms.IntegerField(
        required=True,
        initial=60
    )


class CancelledGearHourForm(forms.ModelForm):
    class Meta:
        model = CancelledGearHour
        fields = (
            'gear_hour',
            'date'
        )

    gear_hour = forms.ModelChoiceField(
        queryset=GearHour.objects.all(),
        label="Gear Hour",
        widget=forms.Select,
        required=True
    )

    date = forms.DateField(
        required=True
    )
