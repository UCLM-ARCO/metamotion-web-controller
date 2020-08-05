from django.urls import path

from . import views

urlpatterns = [
    path('streaming/', views.streaming, name='streaming'),
    path('gathering/', views.gathering, name='gathering'),
]