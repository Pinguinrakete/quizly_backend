import json
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import yt_dlp
from django.contrib.auth.models import User
from rest_framework import serializers

from quiz_app.models import Quiz, QuizQuestions

MAX_VIDEO_DURATION = 15 * 60


class YoutubeURLSerializer(serializers.Serializer):
    """
    Serializer for validating and processing YouTube video URLs.

    This serializer ensures that the provided URL belongs to a valid
    YouTube domain, extracts the video ID, checks the video's duration
    using `yt_dlp`, and ensures it does not exceed the maximum allowed length.

    Upon successful validation, the `create()` method reads a generated JSON
    file containing quiz data (title, description, and questions), and
    creates a corresponding `Quiz` instance with related `QuizQuestions`.

    Fields:
        - url (str): The YouTube video URL to validate.

    Validation:
        - URL must not be empty.
        - Must belong to a recognized YouTube domain
          (e.g. youtube.com, youtu.be).
        - Must contain a valid video ID.
        - Video duration must be readable and not exceed 15 minutes.

    Methods:
        - validate_url(url): Validates and normalizes
          the provided YouTube URL.
        - create(): Reads quiz data from JSON and creates a `Quiz`
          with questions.

    Raises:
        - serializers.ValidationError: If the URL or JSON data is invalid, or
          if the video is too long or cannot be processed.
    """

    url = serializers.CharField(max_length=255)

    def validate_url(self, url):
        if not url:
            raise serializers.ValidationError("URL cannot be empty.")

        parsed_url = urlparse(url)

        valid_domains = ["www.youtube.com",
                         "youtube.com", "m.youtube.com", "youtu.be"]
        if parsed_url.netloc not in valid_domains:
            raise serializers.ValidationError("Invalid YouTube URL domain.")

        if parsed_url.netloc == "youtu.be":
            video_id = parsed_url.path.lstrip("/")
        else:
            query_params = parse_qs(parsed_url.query)
            video_id_list = query_params.get("v")
            if not video_id_list:
                raise serializers.ValidationError("No video ID found in URL.")
            video_id = video_id_list[0]

        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "no_warnings": True,
        }

        video_url = f"https://www.youtube.com/watch?v={video_id}"
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            duration = info.get("duration")

            if duration is None:
                raise serializers.ValidationError(
                    "The length of the video could not be read."
                )
            if duration > MAX_VIDEO_DURATION:
                raise serializers.ValidationError(
                    "Video is longer than 15 minutes.")

        clean_query = urlencode({"v": video_id})
        clean_url = urlunparse(
            ("https", "www.youtube.com", "/watch", "", clean_query, "")
        )

        return clean_url

    def create(self):
        filename = "media/generated_text.txt"

        try:
            with open(filename, "r", encoding="utf-8") as file:
                content = json.load(file)

            title = content.get("title")
            description = content.get("description")
            questions_data = content.get("questions", [])

            if not title or not questions_data:
                raise serializers.ValidationError(
                    "JSON must contain at least 'title' and 'questions'."
                )

            request = self.context.get("request")
            owner = (
                request.user
                if request and request.user.is_authenticated
                else User.objects.first()
            )

            clean_url = self.validated_data["url"]

            quiz = Quiz.objects.create(
                owner=owner,
                title=title,
                description=description,
                video_url=clean_url
            )

            for q in questions_data:
                question = QuizQuestions.objects.create(
                    question_title=q.get("question_title"),
                    question_options=q.get("question_options", []),
                    answer=q.get("answer"),
                )
                quiz.questions.add(question)

            quiz.save()
            return quiz

        except json.JSONDecodeError:
            raise serializers.ValidationError(
                "File does not contain valid JSON.")
        except Exception as e:
            raise serializers.ValidationError(str(e))


class QuestionSerializer(serializers.ModelSerializer):
    """
    Serializer for `QuizQuestions`.

    Ensures each question has exactly 4 answer options.

    Fields:
        - id, question_title, question_options,
          answer, created_at, updated_at
    """

    question_options = serializers.ListField(
        child=serializers.CharField(max_length=255),
        required=False,
        default=list
    )

    class Meta:
        model = QuizQuestions
        fields = [
            "id",
            "question_title",
            "question_options",
            "answer",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "question_title",
            "question_options",
            "answer",
            "created_at",
            "updated_at",
        ]

    def validate_question_options(self, value):
        if len(value) != 4:
            raise serializers.ValidationError(
                "Each question must have exactly 4 answer options."
            )
        return value


class CreateQuizSerializer(serializers.ModelSerializer):
    """
    Serializer for `Quiz` objects with related questions.

    Includes nested `QuestionSerializer` for handling quiz questions.

    Fields:
        - id, title, description, created_at, updated_at, video_url, questions
    """

    questions = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = [
            "id",
            "title",
            "description",
            "created_at",
            "updated_at",
            "video_url",
            "questions",
        ]
        read_only_fields = [
            "id",
            "title",
            "description",
            "created_at",
            "updated_at",
            "video_url",
            "questions",
        ]


class QuestionForQuizzesSerializer(serializers.ModelSerializer):
    """
    Serializer for `QuizQuestions` used in quizzes.

    Ensures exactly 4 answer options per question.

    Fields:
        - id, question_title, question_options, answer
    """

    question_options = serializers.ListField(
        child=serializers.CharField(max_length=255),
        required=False,
        default=list
    )

    class Meta:
        model = QuizQuestions
        fields = ["id", "question_title", "question_options", "answer"]
        read_only_fields = ["id", "question_title",
                            "question_options", "answer"]

    def validate_question_options(self, value):
        if len(value) != 4:
            raise serializers.ValidationError(
                "Each question must have exactly 4 answer options."
            )
        return value


class MyQuizzesSerializer(serializers.ModelSerializer):
    """
    Serializer for `Quiz` with nested questions.

    Uses `QuestionForQuizzesSerializer` for quiz questions.

    Fields:
        - id, title, description, created_at, updated_at, video_url, questions
    """

    questions = QuestionForQuizzesSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = [
            "id",
            "title",
            "description",
            "created_at",
            "updated_at",
            "video_url",
            "questions",
        ]
        read_only_fields = [
            "id",
            "title",
            "description",
            "created_at",
            "updated_at",
            "video_url",
            "questions",
        ]


class QuizSinglePatchSerializer(serializers.ModelSerializer):
    """
    Serializer for partially updating a `Quiz`.

    Allows updating the `title` field only.
    Allows updating the `description` field only.

    Fields:
        - title
        - description
    """

    class Meta:
        model = Quiz
        fields = [
            "title",
            "description",
            "created_at",
            "updated_at",
            "video_url",
            "questions",
        ]
        read_only_fields = ["id", "created_at",
                            "updated_at", "video_url", "questions"]
