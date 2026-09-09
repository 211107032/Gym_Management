from django.urls import path
from . import views

app_name = 'workouts'

urlpatterns = [
    path('', views.workout_list_view, name='list'),
    path('add/', views.workout_create_view, name='create'),
    path('<int:pk>/', views.workout_detail_view, name='detail'),
    path('progress/', views.progress_list_view, name='progress'),
    path('progress/api/<int:member_id>/', views.progress_chart_data, name='chart_data'),
]
