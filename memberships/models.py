from django.db import models
from django.utils import timezone
from datetime import timedelta
from members.models import Member

class MembershipPlan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    duration_days = models.PositiveIntegerField(help_text='Duration in days, e.g. 30, 90, 365')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.TextField(help_text='Features comma or newline separated', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_features_list(self):
        if not self.features:
            return []
        return [f.strip() for f in self.features.replace('\r', '').split('\n') if f.strip()]

    def __str__(self):
        return f"{self.name} ({self.duration_days} Days - ₹{self.price})"


class MemberSubscription(models.Model):
    class StatusChoices(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        EXPIRED = 'EXPIRED', 'Expired'
        CANCELLED = 'CANCELLED', 'Cancelled'
        PENDING = 'PENDING', 'Pending'

    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='subscriptions')
    membership_plan = models.ForeignKey(MembershipPlan, on_delete=models.PROTECT, related_name='subscriptions')
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.end_date and self.start_date and self.membership_plan:
            self.end_date = self.start_date + timedelta(days=self.membership_plan.duration_days)
        if not self.price:
            self.price = self.membership_plan.price
        self.final_amount = self.price - self.discount

        # Auto update status if expired
        today = timezone.now().date()
        if self.end_date < today and self.status == self.StatusChoices.ACTIVE:
            self.status = self.StatusChoices.EXPIRED

        super().save(*args, **kwargs)

        # Update member status
        if self.status == self.StatusChoices.ACTIVE:
            self.member.status = Member.StatusChoices.ACTIVE
            self.member.save()

    @property
    def remaining_days(self):
        today = timezone.now().date()
        if self.end_date < today:
            return 0
        return (self.end_date - today).days

    @property
    def is_expiring_soon(self):
        return 0 < self.remaining_days <= 7 and self.status == self.StatusChoices.ACTIVE

    def __str__(self):
        return f"{self.member.full_name} - {self.membership_plan.name} ({self.status})"
