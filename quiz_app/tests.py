from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch, MagicMock
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from quiz_app.models import Quiz, QuizQuestions

User = get_user_model()

class CreateQuizViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.force_authenticate(user=self.user)
        self.url = reverse('create-quiz')
        self.valid_payload = {"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}
        self.invalid_payload = {"url": "https://www.invalid.com/watch?v=123"}

    @patch("quiz_app.api.views.yt_dlp.YoutubeDL")
    @patch("quiz_app.api.views.whisper.load_model")
    @patch("quiz_app.api.views.AudioQuestionGenerator.generate_questions_gemini")
    def test_create_quiz_success(self, mock_generate_gemini, mock_whisper_model, mock_yt_dlp):
        """Tests successful creation of a quiz (all external services mocked)."""

        mock_yt_dlp.return_value.__enter__.return_value.extract_info.return_value = {'duration': 60}

        mock_model_instance = MagicMock()
        mock_model_instance.transcribe.return_value = {"text": "This is a test transcript."}
        mock_whisper_model.return_value = mock_model_instance
        mock_generate_gemini.return_value = None

        with patch("builtins.open", new_callable=MagicMock) as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = '''
            {
                "title": "Test Quiz",
                "description": "Short description.",
                "questions": [
                    {
                        "question_title": "What is 2+2?",
                        "question_options": ["1", "2", "3", "4"],
                        "answer": "4"
                    }
                ]
            }
            '''
            response = self.client.post(self.url, self.valid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "Test Quiz")
        self.assertEqual(len(response.data['questions']), 1)

    def test_create_quiz_invalid_url(self):
        """Tests that an invalid URL is correctly rejected."""
        response = self.client.post(self.url, self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid YouTube URL domain", str(response.data))

    @patch("quiz_app.api.views.yt_dlp.YoutubeDL")
    def test_video_too_long(self, mock_yt_dlp):
        """Tests rejection of a video longer than 15 minutes."""
        mock_yt_dlp.return_value.__enter__.return_value.extract_info.return_value = {'duration': 3600}
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Video is longer than 15 minutes", str(response.data))


class MyQuizzesViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        Quiz.objects.create(owner=self.user, title='Quiz 1', description='First quiz')
        Quiz.objects.create(owner=self.user, title='Quiz 2', description='Second quiz')
        
        self.url = reverse('quizzes-view')
    
    def test_authenticated_user_can_retrieve_their_quizzes(self):
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)      
        self.assertEqual(len(response.data), 2)
        
        for quiz in response.data:
            self.assertIn('title', quiz)
    
    def test_unauthenticated_user_cannot_access_quizzes(self):
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class QuizSingleViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

        self.quiz = Quiz.objects.create(
            owner=self.user,
            title="Test Quiz",
            description="Test Description",
            video_url="http://example.com/video"
        )

        self.question = QuizQuestions.objects.create(
            question_title="Sample Question",
            question_options=["A", "B", "C", "D"],
            answer="A"
        )

        self.quiz.questions.add(self.question)
        self.quiz.save()

        self.url = reverse('quiz-single-view', kwargs={'pk': self.quiz.id})

    def test_get_quiz(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.quiz.id)
        self.assertEqual(response.data['title'], self.quiz.title)
        self.assertIn('questions', response.data)
        self.assertEqual(len(response.data['questions']), 1)

    def test_get_nonexistent_quiz(self):
        url = reverse('quiz-single-view', kwargs={'pk': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_updates_title_and_description_only(self):
        payload = {"title": "New Title", "description": "New Description", "video_url": "http://hack.com"}
        response = self.client.patch(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.quiz.refresh_from_db()
        self.assertEqual(self.quiz.title, "New Title")
        self.assertEqual(self.quiz.description, "New Description")
        self.assertEqual(self.quiz.video_url, "http://example.com/video")

    def test_patch_cannot_modify_questions(self):
        new_question = QuizQuestions.objects.create(
            question_title="New Q",
            question_options=["A", "B", "C", "D"],
            answer="B"
        )
        payload = {"questions": [new_question.id]}
        response = self.client.patch(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.quiz.refresh_from_db()
        self.assertEqual(self.quiz.questions.count(), 1) 

    def test_delete_quiz(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Quiz.objects.filter(id=self.quiz.id).exists())

    def test_get_nonexistent_quiz(self):
        url = reverse('quiz-single-view', kwargs={'pk': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)