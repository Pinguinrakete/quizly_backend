from django.db import models

class QuestionOptionDetails(models.Model):
    """
    Represents a single answer option for a quiz question.

    Attributes:
        option_text (str): The text content of the option (e.g., "Option A").
    
    Methods:
        __str__: Returns a readable string representation of the option text.
    """
    option_text = models.CharField(max_length=255)

    def __str__(self):
        return self.option_text
    

class QuizQuestionDetails(models.Model):
    """
    Represents a quiz question along with its options and correct answer.

    Attributes:
        question_title (str): The text of the question (e.g., "What is the capital of France?").
        question_options (ManyToManyField): The possible answer options related to the question.
        answer (str): The correct answer to the question.
        created_at (datetime): The timestamp when the question was created.
        updated_at (datetime): The timestamp when the question was last updated.

    Methods:
        clean: Validates that each question must have exactly 4 answer options.
        __str__: Returns the string representation of the question title.
    """
    question_title = models.CharField(max_length=255)
    question_options = models.ManyToManyField(QuestionOptionDetails, blank=True)
    answer = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        """
        Validates that the question has exactly 4 answer options.
        """
        if self.pk and self.question_options.count() != 4:
            from django.core.exceptions import ValidationError
            raise ValidationError("Each question must have exactly 4 answer options.")

    def __str__(self):
        return self.question_title
    

class Quiz(models.Model):
    """
    Represents a quiz consisting of multiple questions and optional metadata.

    Attributes:
        title (str): The title of the quiz.
        description (str): A short description of the quiz.
        created_at (datetime): The timestamp when the quiz was created.
        updated_at (datetime): The timestamp when the quiz was last updated.
        video_url (str): A video URL associated with the quiz, if applicable.
        questions (ManyToManyField): The set of quiz questions related to this quiz.

    Methods:
        __str__: Returns the string representation of the quiz title.
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    video_url = models.CharField(max_length=255)
    questions = models.ManyToManyField(QuizQuestionDetails, blank=True)
    
    def __str__(self):
        return self.title