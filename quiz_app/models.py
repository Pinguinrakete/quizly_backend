from django.db import models

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    video_url = models.CharField(max_length=255)
    questions = models.ManyToManyField(QuizQuestionDetails, blank=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)