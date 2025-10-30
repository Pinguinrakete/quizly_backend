from rest_framework import serializers
from quiz_app.models import Quiz, QuizQuestions


class YoutubeURLSerializer(serializers.ModelSerializer):
    url = serializers.CharField(max_length=255)




    
class QuestionSerializer(serializers.ModelSerializer):
    question_options = serializers.ListField(child=serializers.CharField(max_length=255), required=False, default=list)

    class Meta:
        model = QuizQuestions
        fields = ['id', 'question_title','question_options', 'answer', 'created_at', 'updated_at']

    def validate_question_options(self, value):
        if len(value) != 4:
            raise serializers.ValidationError("Each question must have exactly 4 answer options.")
        return value
    

class CreateQuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True) 

    class Meta:
        model = Quiz
        fields = ['id', 'title','description', 'created_at', 'updated_at', 'video_url', 'questions']