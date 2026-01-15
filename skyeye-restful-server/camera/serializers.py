from rest_framework import serializers
from .models import *


class CameraViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CameraView
        fields = '__all__'