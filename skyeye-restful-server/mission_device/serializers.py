from rest_framework import serializers
from .models import *


class MissionDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Missiondevice
        fields = '__all__'


class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = '__all__'


class MissionDeviceDataLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissiondeviceDataLog
        fields = '__all__'
