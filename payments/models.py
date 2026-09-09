from django.db import models
from django.utils import timezone
from members.models import Member
from memberships.models import MemberSubscription

class Payment(models.Model):
    class MethodChoices(models.TextChoices):
        CASH = 'CASH', 'Cash'
        UPI = 'UPI', 'UPI'
        CARD = 'CARD', 'Card'
        BANK_TRANSFER = 'BANK_TRANSFER', 'Bank Transfer'
        ONLINE = 'ONLINE', 'Online'

    class StatusChoices(models.TextChoices):
        PAID = 'PAID', 'Paid'
        PENDING = 'PENDING', 'Pending'
        FAILED = 'FAILED', 'Failed'
        REFUNDED = 'REFUNDED', 'Refunded'

    payment_id = models.CharField(max_length=20, unique=True, editable=False)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='payments')
    subscription = models.ForeignKey(MemberSubscription, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=MethodChoices.choices, default=MethodChoices.UPI)
    payment_date = models.DateField(default=timezone.now)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.PAID)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.payment_id:
            last_pay = Payment.objects.all().order_by('id').last()
            new_id = (last_pay.id + 1) if (last_pay and last_pay.id) else 1
            self.payment_id = f"PAY-{new_id:06d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.payment_id} - {self.member.full_name} (₹{self.amount})"
