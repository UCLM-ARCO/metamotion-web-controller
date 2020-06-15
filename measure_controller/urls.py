from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('stop/', views.gathering, name='gathering'),
]