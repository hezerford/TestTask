from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import LessonView
from .serializers import LessonViewSerializer

class LessonViewListAPIView(generics.ListAPIView):
    serializer_class = LessonViewSerializer
    permission_classes = [IsAuthenticated]

    # Записи о просмотре уроков, к которым пользователь имеет доступ
    def get_queryset(self):
        user = self.request.user
        # Фильтрация всех записей о просмотре уроков, к которым у пользователя есть доступ
        queryset = LessonView.objects.filter(user=user)
        return queryset

class LessonViewByProductListAPIView(generics.ListAPIView):
    serializer_class = LessonViewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        user = self.request.user
        queryset = LessonView.objects.filter(lesson__products__id=product_id, user=user)
        return queryset
    