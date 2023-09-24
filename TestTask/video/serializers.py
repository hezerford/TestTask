from rest_framework import serializers
from .models import *

class LessonViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonView
        fields = ['__all__'] # Включаются все поля

class ProductStatSerializer(serializers.ModelSerializer):
    total_lessons_viewed = serializers.SerializerMethodField()
    total_view_time = serializers.SerializerMethodField()
    num_students = serializers.SerializerMethodField()
    purchase_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'total_lessons_viewed', 'total_view_time', 'num_students', 'purchase_percentage']

    # Количество просмотренных уроков от всех учеников
    def get_num_lessons_viewed(self, obj):
        total_lessons_viewed = LessonView.objects.filter(lesson__products=obj, is_viewed=True)\
            .aggregate(Sum('viewed_percentage'))['viewed_percentage__sum']
        return total_lessons_viewed if total_lessons_viewed is not None else 0

    # Общее время просмотра для всех уроков в продуктах
    def get_total_view_time(self, obj):
        total_view_time = LessonView.objects.filter(lesson__products=obj)\
            .aggregate(Sum('view_time'))['view_time__sum']
        return total_view_time if total_view_time is not None else 0
    
    # Количество учеников, имеющих доступ к продукту
    def get_num_students(self, obj):
        num_students = obj.access_users.count()
        return num_students
    
    # Процент приобретения продукта
    def get_purchase_percentage(self, obj):
        total_users = User.objects.count()
        if total_users > 0:
            num_accesses = obj.access_users.count()
            purchase_percentage = (num_accesses / total_users) * 100
            return purchase_percentage
        return 0