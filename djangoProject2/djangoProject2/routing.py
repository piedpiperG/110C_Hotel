from django.urls import path

from djangoProject2 import consumers

websocket_urlpatterns = [
    path('room/hony', consumers.ChatConsumer.as_asgi())
]