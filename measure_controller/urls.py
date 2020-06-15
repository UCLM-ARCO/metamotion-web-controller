from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('gathering/', views.gathering, name='gathering'),
]