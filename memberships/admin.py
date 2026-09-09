from django.contrib import admin
from .models import MembershipPlan, MemberSubscription

@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration_days', 'price', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')

@admin.register(MemberSubscription)
class MemberSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('member', 'membership_plan', 'start_date', 'end_date', 'final_amount', 'status')
    list_filter = ('status', 'membership_plan', 'start_date')
    search_fields = ('member__member_id', 'member__user__first_name', 'member__user__last_name')
