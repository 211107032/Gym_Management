from django import forms
from .models import WorkoutPlan, WorkoutExercise, MemberProgress

class WorkoutPlanForm(forms.ModelForm):
    class Meta:
        model = WorkoutPlan
        fields = ['member', 'trainer', 'name', 'description', 'goal']
        widgets = {
            'member': forms.Select(attrs={'class': 'form-select'}),
            'trainer': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'goal': forms.TextInput(attrs={'class': 'form-control'}),
        }

class WorkoutExerciseForm(forms.ModelForm):
    class Meta:
        model = WorkoutExercise
        fields = ['exercise_name', 'muscle_group', 'sets', 'repetitions', 'weight', 'duration', 'rest_time', 'instructions']
        widgets = {
            'exercise_name': forms.TextInput(attrs={'class': 'form-control'}),
            'muscle_group': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Chest, Legs, Arms'}),
            'sets': forms.NumberInput(attrs={'class': 'form-control'}),
            'repetitions': forms.NumberInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Minutes'}),
            'rest_time': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Seconds'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class MemberProgressForm(forms.ModelForm):
    class Meta:
        model = MemberProgress
        fields = ['member', 'date', 'weight', 'height', 'body_fat_percentage', 'chest', 'waist', 'arms', 'thighs', 'notes']
        widgets = {
            'member': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'body_fat_percentage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'chest': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'waist': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'arms': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'thighs': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
