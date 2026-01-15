from .views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register('helikite', HelikiteViewSet)
urlpatterns = router.urls
