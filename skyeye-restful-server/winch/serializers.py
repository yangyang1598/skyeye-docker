from rest_framework import serializers
from .models import *


class WinchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Winch
        fields = '__all__'


class WinchDataLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WinchDataLog
        fields = '__all__'
