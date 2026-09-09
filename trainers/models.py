from django.db import models
from django.conf import settings
from django.utils import timezone
from members.models import Member

class Trainer(models.Model):
    trainer_id = models.CharField(max_length=20, unique=True, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='trainer_profile'
    )
    specialization = models.CharField(max_length=100)
    experience = models.PositiveIntegerField(help_text='Years of experience')
    qualification = models.CharField(max_length=150)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    joining_date = models.DateField(default=timezone.now)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    availability = models.CharField(max_length=100, default='6:00 AM - 2:00 PM / 4:00 PM - 10:00 PM')
    profile_picture = models.ImageField(upload_to='trainers/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.trainer_id:
            last_t = Trainer.objects.all().order_by('id').last()
            new_id = (last_t.id + 1) if (last_t and last_t.id) else 1
            self.trainer_id = f"TRN-{new_id:04d}"
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return self.user.get_full_name_or_username()

    def __str__(self):
        return f"{self.trainer_id} - {self.full_name} ({self.specialization})"


class TrainerAssignment(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='assigned_members')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='assigned_trainers')
    assigned_date = models.DateField(default=timezone.now)

    class Meta:
        unique_together = ('trainer', 'member')

    def __str__(self):
        return f"{self.trainer.full_name} -> {self.member.full_name}"
