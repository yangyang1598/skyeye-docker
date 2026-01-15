from .views import *
from rest_framework import routers
from django.urls import include, path, re_path
from django.contrib import admin

router = routers.SimpleRouter()
router.register('detection', DetectionView)
urlpatterns = router.urls
