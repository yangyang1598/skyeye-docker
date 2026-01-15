from .views import *
from rest_framework import routers
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'camera_view', CameraViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('camera_view', CameraViewSet.as_view({'post':'create', 'delete':'delete'})),
]