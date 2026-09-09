from django.contrib import admin
from .models import Member

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('member_id', 'full_name', 'phone', 'email', 'status', 'joining_date')
    list_filter = ('status', 'gender', 'joining_date')
    search_fields = ('member_id', 'user__first_name', 'user__last_name', 'user__username', 'phone', 'email')
    ordering = ('-joining_date',)
