from django.urls import re_path

from .consumers import MemoryGameConsumer

websocket_urlpatterns = [
    # re_path(r'ws/game$', MemoryGameConsumer.as_asgi()),
    re_path(r'ws/game/(?P<game_id>\w+)/$', MemoryGameConsumer.as_asgi()),
    # re_path(r'ws/live-session/(?P<session_id>\w+)/$', LiveSessionConsumer.as_asgi()),
]