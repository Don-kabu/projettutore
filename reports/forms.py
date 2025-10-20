from django import forms
from .models import Fuite

class FuiteForm(forms.ModelForm):
    class Meta:
        model = Fuite
        fields = ['quartier','photo','description','address']

class complaintForm(forms.ModelForm):
    class Meta:
        model = Fuite
        fields = ['complaint_name','phone','is_owner',"commune",'email']


class OptForm(forms.Form):
    otp = forms.CharField(max_length=7,min_length=5)