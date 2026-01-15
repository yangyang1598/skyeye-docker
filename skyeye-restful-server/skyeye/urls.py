from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register('site', SiteViewSet)
router.register('poi', PoiViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('poi', PoiViewSet.as_view({'post':'create', 'patch':'partial_update','delete':'delete'})),
]