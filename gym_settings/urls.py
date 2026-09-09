from django.urls import path
from . import views

app_name = 'gym_settings'

urlpatterns = [
    path('', views.gym_settings_view, name='index'),
]
