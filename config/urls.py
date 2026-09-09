from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

def custom_403_view(request, exception=None):
    return render(request, '403.html', status=403)

def custom_500_view(request):
    return render(request, '500.html', status=500)

handler404 = 'config.urls.custom_404_view'
handler403 = 'config.urls.custom_403_view'
handler500 = 'config.urls.custom_500_view'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('accounts/', include('accounts.urls')),
    path('members/', include('members.urls')),
    path('memberships/', include('memberships.urls')),
    path('attendance/', include('attendance.urls')),
    path('payments/', include('payments.urls')),
    path('trainers/', include('trainers.urls')),
    path('workouts/', include('workouts.urls')),
    path('reports/', include('reports.urls')),
    path('notifications/', include('notifications.urls')),
    path('audit-logs/', include('audit_logs.urls')),
    path('settings/', include('gym_settings.urls')),
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
