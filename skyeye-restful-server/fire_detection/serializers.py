from rest_framework import serializers
from .models import Detection


class DetectionSerializer(serializers.ModelSerializer):
    # image = serializers.ImageField(use_url=True)

    class Meta:
        model = Detection
        fields = '__all__'
