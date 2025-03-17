from rest_framework import serializers
from .models import Serial

class SerialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Serial
        fields = '__all__'