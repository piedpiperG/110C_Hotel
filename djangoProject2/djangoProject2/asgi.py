"""
ASGI config for djangoProject2 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoProject2.settings")

# application = get_asgi_application()


from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from djangoProject2 import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webSocket.settings')

# application = get_asgi_application()
application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': URLRouter(routing.websocket_urlpatterns),
})
