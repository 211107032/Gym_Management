from django.contrib import admin
from .models import WorkoutPlan, WorkoutExercise, MemberProgress

class WorkoutExerciseInline(admin.TabularInline):
    model = WorkoutExercise
    extra = 1

@admin.register(WorkoutPlan)
class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'member', 'trainer', 'goal', 'created_at')
    search_fields = ('name', 'member__member_id', 'member__user__first_name')
    inlines = [WorkoutExerciseInline]

@admin.register(MemberProgress)
class MemberProgressAdmin(admin.ModelAdmin):
    list_display = ('member', 'date', 'weight', 'height', 'bmi', 'body_fat_percentage')
    list_filter = ('date',)
    search_fields = ('member__member_id', 'member__user__first_name')
