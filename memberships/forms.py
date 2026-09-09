from django import forms
from .models import MembershipPlan, MemberSubscription

class MembershipPlanForm(forms.ModelForm):
    class Meta:
        model = MembershipPlan
        fields = ['name', 'description', 'duration_days', 'price', 'features', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'duration_days': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'features': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter features, one per line'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class MemberSubscriptionForm(forms.ModelForm):
    class Meta:
        model = MemberSubscription
        fields = ['member', 'membership_plan', 'start_date', 'discount', 'status']
        widgets = {
            'member': forms.Select(attrs={'class': 'form-select'}),
            'membership_plan': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
