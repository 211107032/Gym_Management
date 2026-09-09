from django.contrib import admin
from .models import GymSetting

@admin.register(GymSetting)
class GymSettingAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'currency', 'tax_percentage', 'updated_at')
