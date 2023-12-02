import os
import django

# 首先设置 Django 环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel.settings')
# 然后初始化 Django
django.setup()

# 现在可以安全地导入依赖于 Django 的模块
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from hotel.consumers import MyConsumer  # 确保导入了你的 Consumer

import os
import django
from django.core.asgi import get_asgi_application
from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler

# 首先设置 Django 环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel.settings')
# 然后初始化 Django
django.setup()

# 接下来是 ASGI 应用的其余部分
application = ProtocolTypeRouter({
    "http": ASGIStaticFilesHandler(get_asgi_application()),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/some_path/", MyConsumer.as_asgi()),
        ])
    ),
})

