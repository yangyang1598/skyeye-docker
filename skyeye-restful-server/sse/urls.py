from django.urls import include, path
from .views import *
import django_eventstream

urlpatterns = [
    path('messages/<str:channels_id>', messages),
    path('events/<str:channels_id>', include(django_eventstream.urls), {
        'format-channels': ['channels-{channels_id}']
    }),
]
