"""
ASGI config for SoftwareDevProject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
import django
from channels.routing import get_default_application, ProtocolTypeRouter
from django.core.asgi import get_asgi_application

import apps.market.routing


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoProject.settings")
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": apps.market.routing.websocket_urlpatterns,
})
