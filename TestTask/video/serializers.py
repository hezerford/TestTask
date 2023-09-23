from rest_framework import serializers
from .models import LessonView

class LessonViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonView
        fields = ['__all__'] # Включаются все поля