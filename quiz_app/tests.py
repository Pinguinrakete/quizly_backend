from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch, MagicMock
from django.contrib.auth import get_user_model

User = get_user_model()

class CreateQuizViewTest(APITestCase):
    def setUp(self):
        # Create and authenticate test user
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

        # Mock YouTube download
        mock_yt_dlp.return_value.__enter__.return_value.extract_info.return_value = {'duration': 60}

        # Mock Whisper transcription
        mock_model_instance = MagicMock()
        mock_model_instance.transcribe.return_value = {"text": "This is a test transcript."}
        mock_whisper_model.return_value = mock_model_instance

        # Mock Gemini question generation
        mock_generate_gemini.return_value = None

        # Mock JSON file with simulated content
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

        # Check expected result
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