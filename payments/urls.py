from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('', views.payment_list_view, name='list'),
    path('add/', views.payment_create_view, name='create'),
    path('<int:pk>/receipt/', views.payment_receipt_view, name='receipt'),
]
