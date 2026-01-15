from .views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register('log', StatusLogViewSet)
urlpatterns = router.urls
