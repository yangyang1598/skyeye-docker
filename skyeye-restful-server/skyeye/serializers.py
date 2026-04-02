from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import *


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = '__all__'

class PoiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poi
        fields = '__all__'

class Scan360ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scan360Config
        fields = '__all__'
