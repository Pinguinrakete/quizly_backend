from django.db import models

class QuestionOptionDetails(models.Model):
    option_text = models.CharField(max_length=255)

    def __str__(self):
        return self.option_text
    

class QuizQuestionDetails(models.Model):
    question_title = models.CharField(max_length=255)
    question_options = models.ManyToManyField(QuestionOptionDetails, blank=True)
    answer = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.pk and self.question_options.count() != 4:
            from django.core.exceptions import ValidationError
            raise ValidationError("Each question must have exactly 4 answer options.")

    def __str__(self):
        return self.question_title
    

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    video_url = models.CharField(max_length=255)
    questions = models.ManyToManyField(QuizQuestionDetails, blank=True)
    
    def __str__(self):
        return self.title