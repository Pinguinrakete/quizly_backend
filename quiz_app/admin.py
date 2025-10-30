from django.contrib import admin
from .models import Quiz, QuizQuestionDetails, QuestionOptionDetails

admin.site.register(Quiz)
admin.site.register(QuizQuestionDetails)
admin.site.register(QuestionOptionDetails)