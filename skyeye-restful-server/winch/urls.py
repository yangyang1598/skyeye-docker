from .views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register('winch', WinchViewSet)
router.register('winch_log', WinchDataLogViewSet)
urlpatterns = router.urls
