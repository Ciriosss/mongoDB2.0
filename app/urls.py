from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name = 'home'),
    path('profit/', views.profit, name = 'profit'),
    path('orderBook/', views.orderBook, name = 'orderBook')
]