from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register('site', SiteViewSet)
router.register('poi', PoiViewSet)

urlpatterns = [
    path('', include(router.urls)),
]