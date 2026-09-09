from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('', views.attendance_list_view, name='list'),
    path('check-in/', views.check_in_view, name='check_in'),
    path('<int:pk>/check-out/', views.check_out_view, name='check_out'),
]
