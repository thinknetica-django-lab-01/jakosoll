"""
ASGI config for django_lab project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter
from chat.routing import websockets

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_lab.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": websockets,
    # Just HTTP for now. (We can add other protocols later.)
})
