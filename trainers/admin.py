from django.contrib import admin
from .models import Trainer, TrainerAssignment

@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ('trainer_id', 'full_name', 'specialization', 'experience', 'phone', 'joining_date')
    list_filter = ('specialization', 'joining_date')
    search_fields = ('trainer_id', 'user__first_name', 'user__last_name', 'specialization')

@admin.register(TrainerAssignment)
class TrainerAssignmentAdmin(admin.ModelAdmin):
    list_display = ('trainer', 'member', 'assigned_date')
    search_fields = ('trainer__user__first_name', 'member__user__first_name')
