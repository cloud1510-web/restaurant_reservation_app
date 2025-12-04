from django import forms
from .models import Branch, Table, MenuItem, Reservation

class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['name', 'slug', 'address', 'timezone']


class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['branch', 'name', 'capacity', 'status', 'x', 'y']


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['branch', 'name', 'description', 'price', 'available']


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['branch', 'party_size', 'date', 'time']

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
