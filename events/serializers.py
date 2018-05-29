from rest_framework import serializers
from .models import band, venue

class bandSerializer(serializers.ModelSerializer):
    class Meta:
        model = band
        fields = '__all__'

class venueSerializer(serializers.ModelSerializer):
    class Meta:
        model = venue
        fields = '__all__'

