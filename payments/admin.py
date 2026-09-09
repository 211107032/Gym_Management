from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'member', 'amount', 'payment_method', 'payment_date', 'status')
    list_filter = ('payment_method', 'status', 'payment_date')
    search_fields = ('payment_id', 'member__member_id', 'member__user__first_name', 'member__user__last_name', 'transaction_id')
    date_hierarchy = 'payment_date'
