from django import forms
from django.contrib.auth.models import User
from .models import StaffProfile

class StaffUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    is_staff = forms.BooleanField(required=False, initial=True)
    is_superuser = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'is_staff', 'is_superuser']

class StaffProfileForm(forms.ModelForm):
    class Meta:
        model = StaffProfile
        fields = ['full_name', 'position', 'shift']
