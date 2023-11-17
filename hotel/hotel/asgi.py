# hotel/asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from hotel.consumers import MyConsumer  # 确保导入了你的 Consumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/some_path/", MyConsumer.as_asgi()),
        ])
    ),
})
