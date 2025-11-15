from unittest.mock import MagicMock, patch

from django.contrib.auth.models import User
from django.db import DatabaseError
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from quiz_app.models import Quiz, QuizQuestions
from quiz_app.api.permissions import IsOwner


class CreateQuizViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse("create-quiz")
        self.valid_payload = {
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        }
        self.invalid_payload = {"url": "https://www.invalid.com/watch?v=123"}

    @patch(
        "yt_dlp.YoutubeDL"
        )
    @patch(
        "whisper.load_model"
        )
    @patch(
        "quiz_app.api.views.AudioQuestionGenerator.generate_questions_gemini"
        )
    def test_create_quiz_success(
        self,
        mock_generate_gemini,
        mock_whisper_model,
        mock_yt_dlp,
    ):
        """Tests successful creation of a quiz
           (all external services mocked)."""

        extract_info_mock = (
            mock_yt_dlp.return_value.__enter__.return_value.extract_info
        )
        extract_info_mock.return_value = {"duration": 60}

        mock_model_instance = MagicMock()
        mock_model_instance.transcribe.return_value = {
            "text": "This is a test transcript."
            }
        mock_whisper_model.return_value = mock_model_instance

        mock_generate_gemini.return_value = None

        with patch("builtins.open", new_callable=MagicMock) as mock_open:
            mock_read = mock_open.return_value.__enter__.return_value.read
            mock_read.return_value = """\
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
            """

            response = self.client.post(
                self.url,
                self.valid_payload,
                format="json"
                )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
            )
        self.assertEqual(
            response.data["title"],
            "Test Quiz"
            )
        self.assertEqual(
            len(response.data["questions"]),
            1)

    def test_create_quiz_invalid_url(self):
        response = self.client.post(
            self.url,
            self.invalid_payload,
            format="json"
            )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
            )
        self.assertIn(
            "Invalid YouTube URL domain",
            str(response.data)
            )

    @patch("yt_dlp.YoutubeDL")
    def test_video_too_long(self, mock_yt_dlp):
        """Tests rejection of a video
           longer than 15 minutes."""

        mock_extract_info = (
            mock_yt_dlp.return_value.__enter__.return_value.extract_info
        )
        mock_extract_info.return_value = {"duration": 3600}

        response = self.client.post(
            self.url,
            self.valid_payload,
            format="json"
            )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
            )
        self.assertIn(
            "Video is longer than 15 minutes",
            str(response.data)
            )


class MyQuizzesViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass"
            )
        Quiz.objects.create(
            owner=self.user,
            title="Quiz 1",
            description="First quiz"
            )
        Quiz.objects.create(
            owner=self.user,
            title="Quiz 2",
            description="Second quiz"
            )

        self.url = reverse("quizzes-view")

    def test_authenticated_user_can_retrieve_their_quizzes(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
            )
        self.assertEqual(len(response.data), 2)
        for quiz in response.data:
            self.assertIn(
                "title",
                quiz
                )

    def test_unauthenticated_user_cannot_access_quizzes(self):
        response = self.client.get(self.url)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
            )


class MyQuizzesViewAdditionalTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1",
            password="pass1"
            )
        self.user2 = User.objects.create_user(
            username="user2",
            password="pass2"
            )

        Quiz.objects.create(
            owner=self.user1,
            title="User1 Quiz 1",
            description="Desc 1"
            )
        Quiz.objects.create(
            owner=self.user1,
            title="User1 Quiz 2",
            description="Desc 2"
            )
        Quiz.objects.create(
            owner=self.user2,
            title="User2 Quiz 1",
            description="Desc 3"
            )

        self.url = reverse("quizzes-view")

    def test_only_user_quizzes_returned(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
            )
        self.assertEqual(len(response.data), 2)
        for quiz in response.data:
            self.assertTrue(quiz["title"].startswith("User1"))

    def test_no_quizzes_returns_empty_list(self):
        user_no_quizzes = User.objects.create_user(
            username="nouser",
            password="pass3"
            )
        self.client.force_authenticate(user=user_no_quizzes)
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
            )
        self.assertEqual(response.data, [])


class QuizSingleViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass"
            )
        self.client.force_authenticate(user=self.user)

        self.quiz = Quiz.objects.create(
            owner=self.user,
            title="Test Quiz",
            description="Test Description",
            video_url="http://example.com/video",
        )

        self.question = QuizQuestions.objects.create(
            question_title="Sample Question",
            question_options=["A", "B", "C", "D"],
            answer="A",
        )

        self.quiz.questions.add(self.question)
        self.quiz.save()

        self.url = reverse("quiz-single-view", kwargs={"pk": self.quiz.id})

    def test_get_quiz(self):
        response = self.client.get(self.url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
            )
        self.assertEqual(
            response.data["id"],
            self.quiz.id
            )
        self.assertEqual(
            response.data["title"],
            self.quiz.title
            )
        self.assertIn(
            "questions",
            response.data
            )
        self.assertEqual(len(response.data["questions"]), 1)

    def test_get_nonexistent_quiz(self):
        url = reverse(
            "quiz-single-view",
            kwargs={"pk": 999}
            )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_updates_title_and_description_only(self):
        payload = {
            "title": "New Title",
            "description": "New Description",
            "video_url": "http://hack.com",
        }
        response = self.client.patch(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.quiz.refresh_from_db()
        self.assertEqual(self.quiz.title, "New Title")
        self.assertEqual(self.quiz.description, "New Description")
        self.assertEqual(self.quiz.video_url, "http://example.com/video")

    def test_patch_cannot_modify_questions(self):
        new_question = QuizQuestions.objects.create(
            question_title="New Q",
            question_options=["A", "B", "C", "D"],
            answer="B",
        )
        payload = {"questions": [new_question.id]}
        response = self.client.patch(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.quiz.refresh_from_db()
        self.assertEqual(self.quiz.questions.count(), 1)

    def test_delete_quiz(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Quiz.objects.filter(id=self.quiz.id).exists())


class IsOwnerPermissionTest(APITestCase):
    def test_is_owner_permission(self):
        UserModel = User

        user = UserModel.objects.create(username="a")
        other = UserModel.objects.create(username="b")

        obj1 = type("X", (), {"owner": user})()
        obj2 = type("X", (), {"owner": other})()

        req = APIRequestFactory().get("/")
        req.user = user

        perm = IsOwner()
        self.assertTrue(perm.has_object_permission(req, None, obj1))
        self.assertFalse(perm.has_object_permission(req, None, obj2))


class QuizSingleViewPermissionAndErrorTests(APITestCase):
    def setUp(self):
        self.user_owner = User.objects.create_user(
            username="owner",
            password="pass1"
            )
        self.user_other = User.objects.create_user(
            username="other",
            password="pass2"
            )
        self.quiz = Quiz.objects.create(
            owner=self.user_owner,
            title="Owner Quiz",
            description="Desc",
            video_url="http://example.com/video"
        )
        self.url = reverse("quiz-single-view", kwargs={"pk": self.quiz.id})

    def test_patch_with_invalid_data_returns_400(self):
        self.client.force_authenticate(user=self.user_owner)
        payload = {"title": ""}
        response = self.client.patch(
            self.url,
            payload,
            format="json"
            )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_patch_unauthenticated_returns_401(self):
        payload = {"title": "New Title"}
        response = self.client.patch(
            self.url,
            payload,
            format="json"
            )
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
            )

    def test_patch_by_non_owner_returns_403(self):
        self.client.force_authenticate(user=self.user_other)
        payload = {"title": "Hack Title"}
        response = self.client.patch(
            self.url,
            payload,
            format="json"
            )
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
            )

    def test_get_by_non_owner_returns_403(self):
        self.client.force_authenticate(user=self.user_other)
        response = self.client.get(self.url)
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
            )

    def test_delete_by_non_owner_returns_403(self):
        self.client.force_authenticate(user=self.user_other)
        response = self.client.delete(self.url)
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
            )

    @patch("quiz_app.models.Quiz.delete")
    def test_delete_database_error_returns_500(self, mock_delete):
        self.client.force_authenticate(user=self.user_owner)
        mock_delete.side_effect = DatabaseError("DB Error")
        response = self.client.delete(self.url)
        self.assertEqual(
            response.status_code,
            status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        self.assertIn("DB Error", str(response.data))
