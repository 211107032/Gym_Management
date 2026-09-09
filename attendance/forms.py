from django import forms
from .models import Attendance
from members.models import Member

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['member', 'date', 'check_in_time', 'check_out_time', 'status']
        widgets = {
            'member': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'check_in_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'check_out_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

class QuickCheckInForm(forms.Form):
    member_identifier = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter Member ID, Phone or Name',
            'autofocus': True,
            'id': 'quick_check_in_input'
        })
    )
