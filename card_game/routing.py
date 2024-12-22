from django.urls import re_path

from .consumers import MemoryGameConsumer

websocket_urlpatterns = [
    re_path(r'ws/game/(?P<game_id>\w+)/$', MemoryGameConsumer.as_asgi()),
]