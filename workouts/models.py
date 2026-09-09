from django.db import models
from django.utils import timezone
from members.models import Member
from trainers.models import Trainer

class WorkoutPlan(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='workout_plans')
    trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_plans')
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    goal = models.CharField(max_length=100, default='General Fitness')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.member.full_name}"


class WorkoutExercise(models.Model):
    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE, related_name='exercises')
    exercise_name = models.CharField(max_length=100)
    muscle_group = models.CharField(max_length=50)
    sets = models.PositiveIntegerField(default=3)
    repetitions = models.PositiveIntegerField(default=10)
    weight = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text='Weight in kg')
    duration = models.PositiveIntegerField(blank=True, null=True, help_text='Duration in minutes')
    rest_time = models.PositiveIntegerField(default=60, help_text='Rest in seconds')
    instructions = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.exercise_name} ({self.muscle_group}) - {self.sets}x{self.repetitions}"


class MemberProgress(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='progress_records')
    date = models.DateField(default=timezone.now)
    weight = models.DecimalField(max_digits=5, decimal_places=2, help_text='Weight in kg')
    height = models.DecimalField(max_digits=5, decimal_places=2, help_text='Height in cm')
    bmi = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    body_fat_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    chest = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    waist = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    arms = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    thighs = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']

    def save(self, *args, **kwargs):
        if self.weight and self.height and self.height > 0:
            height_m = float(self.height) / 100.0
            self.bmi = round(float(self.weight) / (height_m ** 2), 2)
        super().save(*args, **kwargs)

        # Update latest weight/height on Member model
        self.member.weight = self.weight
        self.member.height = self.height
        self.member.save()

    def __str__(self):
        return f"{self.member.full_name} Progress ({self.date}): {self.weight}kg, BMI {self.bmi}"
