from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from .models import GymSetting

class GymSettingForm(forms.ModelForm):
    class Meta:
        model = GymSetting
        fields = ['name', 'logo', 'address', 'phone', 'email', 'opening_time', 'closing_time', 'currency', 'tax_percentage']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'opening_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'closing_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'currency': forms.TextInput(attrs={'class': 'form-control'}),
            'tax_percentage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

@login_required
def gym_settings_view(request):
    if not request.user.is_admin:
        messages.error(request, "Access denied. Only Admin can update gym settings.")
        return redirect('dashboard:index')

    settings_obj = GymSetting.get_settings()
    if request.method == 'POST':
        form = GymSettingForm(request.POST, request.FILES, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Gym settings updated successfully!")
            return redirect('gym_settings:index')
    else:
        form = GymSettingForm(instance=settings_obj)

    return render(request, 'gym_settings/index.html', {'form': form, 'settings_obj': settings_obj})
