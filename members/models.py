from django.db import models
from django.conf import settings
from django.utils import timezone

class Member(models.Model):
    class GenderChoices(models.TextChoices):
        MALE = 'MALE', 'Male'
        FEMALE = 'FEMALE', 'Female'
        OTHER = 'OTHER', 'Other'

    class StatusChoices(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        INACTIVE = 'INACTIVE', 'Inactive'
        SUSPENDED = 'SUSPENDED', 'Suspended'
        EXPIRED = 'EXPIRED', 'Expired'

    member_id = models.CharField(max_length=20, unique=True, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='member_profile'
    )
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GenderChoices.choices, default=GenderChoices.MALE)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField(blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True, null=True)
    joining_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.ACTIVE)
    height = models.DecimalField(max_digits=5, decimal_places=2, help_text='Height in cm', blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, help_text='Weight in kg', blank=True, null=True)
    medical_notes = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='members/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.member_id:
            last_member = Member.objects.all().order_by('id').last()
            if last_member and last_member.id:
                new_id = last_member.id + 1
            else:
                new_id = 1
            self.member_id = f"MEM-{new_id:04d}"
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return self.user.get_full_name_or_username()

    @property
    def active_subscription(self):
        return self.subscriptions.filter(status='ACTIVE').order_by('-end_date').first()

    def __str__(self):
        return f"{self.member_id} - {self.full_name}"
