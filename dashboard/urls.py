from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('api/analytics/', views.chart_analytics_api, name='analytics_api'),
]
