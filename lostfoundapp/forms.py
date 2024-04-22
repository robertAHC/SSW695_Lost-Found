from django import forms
from .models import MissingItem


class MissingItemForm(forms.ModelForm):
    class Meta:
        model = MissingItem
        fields = ['name', 'description', 'color', 'date_lost', 'photo']  # Add 'photo' to fields