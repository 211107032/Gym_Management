from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.report_index_view, name='index'),
    path('export/<str:report_type>/', views.export_csv_view, name='export_csv'),
]
