from django import forms
from .models import Fuite

class FuiteForm(forms.ModelForm):
    class Meta:
        model = Fuite
        fields = ['description', 'photo']