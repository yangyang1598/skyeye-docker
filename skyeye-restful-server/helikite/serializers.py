from rest_framework import serializers
from .models import *


class HelikiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Helikite
        fields = '__all__'