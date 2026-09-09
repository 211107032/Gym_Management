from django.urls import path
from . import views

app_name = 'trainers'

urlpatterns = [
    path('', views.trainer_list_view, name='list'),
    path('add/', views.trainer_create_view, name='create'),
    path('assign/', views.assign_member_view, name='assign'),
    path('<int:pk>/', views.trainer_detail_view, name='detail'),
    path('<int:pk>/edit/', views.trainer_edit_view, name='edit'),
]
