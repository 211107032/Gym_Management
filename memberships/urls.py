from django.urls import path
from . import views

app_name = 'memberships'

urlpatterns = [
    path('plans/', views.plan_list_view, name='plan_list'),
    path('plans/add/', views.plan_create_view, name='plan_create'),
    path('plans/<int:pk>/edit/', views.plan_edit_view, name='plan_edit'),
    path('subscriptions/', views.subscription_list_view, name='subscription_list'),
    path('subscriptions/assign/', views.subscription_create_view, name='subscription_create'),
]
