from rest_framework import serializers
from quiz_app.models import Quiz, QuizQuestions
from urllib.parse import urlparse


class YoutubeURLSerializer(serializers.ModelSerializer):
    url = serializers.CharField(max_length=255)

    class Meta:
        model = Quiz
        fields = ["url"] 

    def validate_url(value):
        if not value:
            raise serializers.ValidationError("URL cannot be empty.")

        parsed_url = urlparse(value)
        valid_domains = ["youtube.com", "www.youtube.com", "youtu.be", "m.youtube.com"]

        if parsed_url.netloc not in valid_domains:
            raise serializers.ValidationError("Invalid YouTube URL.")

        return value


class QuestionSerializer(serializers.ModelSerializer):
    question_options = serializers.ListField(child=serializers.CharField(max_length=255), required=False, default=list)

    class Meta:
        model = QuizQuestions
        fields = ['id', 'question_title','question_options', 'answer', 'created_at', 'updated_at']
        read_only_fields = ['id', 'question_title','question_options', 'answer', 'created_at', 'updated_at']

    def validate_question_options(self, value):
        if len(value) != 4:
            raise serializers.ValidationError("Each question must have exactly 4 answer options.")
        return value
    

class CreateQuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True) 

    class Meta:
        model = Quiz
        fields = ['id', 'title','description', 'created_at', 'updated_at', 'video_url', 'questions']
        read_only_fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'video_url', 'questions']


class QuizSinglePatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['title']
        read_only_fields = ['id', 'description', 'created_at', 'updated_at', 'video_url', 'questions']