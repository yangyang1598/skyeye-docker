"""
ASGI config for server project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
import django
from django.urls import path, re_path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import django_eventstream
from .token_auth import TokenAuthMiddlewareStack

# application = get_asgi_application()
application = ProtocolTypeRouter({
    'http': URLRouter([
        path('events/<channels_id>', TokenAuthMiddlewareStack(
            URLRouter(django_eventstream.routing.urlpatterns)
        ), {'format-channels': ['channels-{channels_id}']}),

        re_path(r'', get_asgi_application()),
    ]),

})
