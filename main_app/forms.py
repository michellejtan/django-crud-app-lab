from django import forms
from .models import Care

class CareForm(forms.ModelForm):
    class Meta:
        model = Care
        fields = ['date', 'time_of_day']
