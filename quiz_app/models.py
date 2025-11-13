from django.contrib.auth.models import User
from django.db import models
from rest_framework.exceptions import ValidationError


class QuizQuestions(models.Model):
    """
    Represents a quiz question with multiple
    choice options and its correct answer.

    Attributes:
        question_title (str): The text of the quiz question
        (e.g., "What is the capital of France?").question_options
        (list of str): A list containing exactly 4 possible
        answer options. answer (str): The correct answer, which
        must match one of the options in `question_options`.
        created_at (datetime): The timestamp when the question
        was created (auto-generated). updated_at (datetime): The
        timestamp when the question was last updated (auto-updated).

    Methods:
        clean(): Ensures that `question_options`
        contains exactly 4 items.
        save(*args, **kwargs): Calls `full_clean`
        before saving to enforce validation.
        __str__(): Returns the `question_title`
        as the string representation of the object.
    """

    question_title = models.CharField(max_length=255)
    question_options = models.JSONField(default=list, blank=True)
    answer = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if len(self.question_options) != 4:
            raise ValidationError(
                "Each question must have exactly 4 answer options."
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.question_title


class Quiz(models.Model):
    """
    Represents a quiz consisting of multiple questions and optional metadata.

    Attributes:
        owner (User): The user who created or owns the quiz.
        title (str): The title of the quiz.
        description (str): A short description of the quiz.
        created_at (datetime): The timestamp when the quiz was created.
        updated_at (datetime): The timestamp when the quiz was last updated.
        video_url (str): A video URL associated with the quiz, if applicable.
        questions (ManyToManyField): The set of quiz questions
        related to this quiz.

    Methods:
        __str__: Returns the string representation of the quiz title.
    """

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quizzes")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    video_url = models.CharField(max_length=255)
    questions = models.ManyToManyField(QuizQuestions, blank=True)

    def __str__(self):
        return self.title
