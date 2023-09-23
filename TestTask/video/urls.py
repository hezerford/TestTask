from django.urls import path
from .views import *

urlpatterns = [
    path('lesson-views/', LessonViewListAPIView.as_view(), name='lesson-view-list'),
    path('lesson-views/<int:product_id>/', LessonViewByProductListAPIView.as_view(), name='lesson-view-by-product-list')
]
