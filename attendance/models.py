from django.db import models
from django.utils import timezone
from members.models import Member

class Attendance(models.Model):
    class StatusChoices(models.TextChoices):
        PRESENT = 'PRESENT', 'Present'
        ABSENT = 'ABSENT', 'Absent'
        LATE = 'LATE', 'Late'

    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField(default=timezone.now)
    check_in_time = models.TimeField(blank=True, null=True)
    check_out_time = models.TimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.PRESENT)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('member', 'date')
        ordering = ['-date', '-check_in_time']

    def __str__(self):
        return f"{self.member.member_id} - {self.date} ({self.get_status_display()})"
