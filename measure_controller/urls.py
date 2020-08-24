from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('streaming/', views.streaming, name='streaming'),
    path('gathering/', views.gathering, name='gathering'),
    path('logging/', views.logging, name='logging'),
]