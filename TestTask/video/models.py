from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    # Доступ к продукту
    access_users = models.ManyToManyField(User, related_name='products_accesed', blank=True) 

class Lesson(models.Model):
    title = models.CharField(max_length=255)
    video_link = models.URLField()
    duration_seconds = models.IntegerField()
    products = models.ManyToManyField(Product)

class LessonView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    view_time = models.DateTimeField()
    is_viewed = models.BooleanField(default=False)
    viewed_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    # Вычисляет процент просмотренного урока
    def calculate_viewed_percentage(self):
        total_duration = self.lesson.duration_seconds
        viewed_duration = (self.view_time - self.lesson.created_at).total_seconds()
        percents = (viewed_duration / total_duration) * 100
        self.viewed_percentage = round(percents, 2)

        if self.viewed_percentage >= 80.00:
            self.is_viewed = True
        else:
            self.is_viewed = False

    def save(self, *args, **kwargs):
        self.calculate_viewed_percentage()
        super().save(*args, **kwargs)