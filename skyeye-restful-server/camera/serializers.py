from rest_framework import serializers
from .models import *

class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = '__all__'

class CameraViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CameraView
        fields = '__all__'