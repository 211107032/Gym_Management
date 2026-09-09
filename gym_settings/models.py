from django.db import models
from datetime import time

class GymSetting(models.Model):
    name = models.CharField(max_length=150, default='Apex Gym & Fitness Center')
    logo = models.ImageField(upload_to='gym_logo/', blank=True, null=True)
    address = models.TextField(default='123 Fitness Avenue, Tech District, City Center')
    phone = models.CharField(max_length=20, default='+1 (555) 019-2834')
    email = models.EmailField(default='contact@apexgym.com')
    opening_time = models.TimeField(default=time(6, 0))
    closing_time = models.TimeField(default=time(22, 0))
    currency = models.CharField(max_length=10, default='₹')
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=18.00)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Enforce single setting instance
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return self.name
