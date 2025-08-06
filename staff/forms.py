from django import forms
from django.contrib.auth.models import User
from .models import Position, StaffProfile, Shift, WorkLog


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = '__all__'

class StaffUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    is_staff = forms.BooleanField(required=False, initial=True)
    is_superuser = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password', 'is_staff', 'is_superuser']

class StaffProfileForm(forms.ModelForm):
    class Meta:
        model = StaffProfile
        fields = ['position', 'hourly_rate', 'phone_number']
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': 'e.g. 91234567'})
        }

class ShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = '__all__'

class WorkLogForm(forms.ModelForm):
    class Meta:
        model = WorkLog
        fields = ['staff', 'shift', 'date', 'clock_in_time', 'clock_out_time', 'is_substitute', 'is_overtime']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'clock_in_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'clock_out_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }