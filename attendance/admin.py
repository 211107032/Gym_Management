from django.contrib import admin
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('member', 'date', 'check_in_time', 'check_out_time', 'status')
    list_filter = ('status', 'date')
    search_fields = ('member__member_id', 'member__user__first_name', 'member__user__last_name')
    date_hierarchy = 'date'
