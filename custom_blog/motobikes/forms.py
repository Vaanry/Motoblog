from django import forms
from .models import Motobike

class MotobikeForm(forms.ModelForm):
    class Meta:
        model = Motobike
        fields = '__all__'
