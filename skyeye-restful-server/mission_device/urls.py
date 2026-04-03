from .views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register('mission_device', MissionDeviceViewSet)
router.register('mission_device_log', MissionDeviceDataLogViewSet)

urlpatterns = router.urls
