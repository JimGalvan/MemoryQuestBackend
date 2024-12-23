from django.urls import path

from . import views

urlpatterns = [
    path('room/', views.create_room, name='home'),
]
