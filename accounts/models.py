from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        STAFF = 'STAFF', 'Staff'
        TRAINER = 'TRAINER', 'Trainer'
        MEMBER = 'MEMBER', 'Member'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.MEMBER,
        help_text='Role for role-based access control'
    )
    phone = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    @property
    def is_staff_user(self):
        return self.role == self.Role.STAFF or self.is_admin

    @property
    def is_trainer(self):
        return self.role == self.Role.TRAINER

    @property
    def is_member(self):
        return self.role == self.Role.MEMBER

    def get_full_name_or_username(self):
        full = f"{self.first_name} {self.last_name}".strip()
        return full if full else self.username

    def __str__(self):
        return f"{self.get_full_name_or_username()} ({self.get_role_display()})"
