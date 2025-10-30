from django.urls import path
from .views import CreateQuizView, MyQuizzesView, QuizSingleView

"""
    URL routes for quiz-related API endpoints.

    Includes endpoints for:
    - Creating a new quiz
    - Retrieving a list of all quizzes
    - Retrieving, updating, or deleting a single quiz by its ID
"""
urlpatterns = [
    path('createQuiz/', CreateQuizView.as_view(), name='create-quiz'),
    path('quizzes/', MyQuizzesView.as_view(), name='quizzes-view'),
    path('quizzes/<int:pk>/', QuizSingleView.as_view(), name='quiz-single-view')
]