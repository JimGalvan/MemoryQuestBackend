from django.urls import path

from . import views

urlpatterns = [
    path('room/', views.create_room, name='home'),
    path('room/<str:room_id>', views.get_room, name='get_room'),
    path('room/join/', views.join_room, name='join_room'),
]
