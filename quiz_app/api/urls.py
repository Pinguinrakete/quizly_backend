from django.urls import path
from .views import CreateQuizView, QuizzesView, QuizSingleView

urlpatterns = [
    path('createQuiz/', CreateQuizView.as_view(), name='create-quiz'),
    path('quizzes/', QuizzesView.as_view(), name='quizzes-view'),
    path('quizzes/<int:pk>/', QuizSingleView.as_view(), name='quiz-single-view')
]