from rest_framework import serializers
from quiz_app.models import Quiz, QuizQuestions
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


class YoutubeURLSerializer(serializers.Serializer):
    url = serializers.CharField(max_length=255)

    def validate_url(self, url):
        if not url:
            raise serializers.ValidationError("URL cannot be empty.")

        parsed_url = urlparse(url)

        valid_domains = ["www.youtube.com", "youtube.com", "m.youtube.com", "youtu.be"]
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

        clean_query = urlencode({"v": video_id})
        clean_url = urlunparse((
            "https",                  # immer https
            "www.youtube.com",         # saubere Domain
            "/watch",                  # Pfad
            '',                        # params
            clean_query,               # query
            ''                         # fragment
        ))

        return clean_url


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