from .permissions import IsOwner
from .serializers import YoutubeURLSerializer, CreateQuizSerializer, MyQuizzesSerializer, QuizSinglePatchSerializer
from .utils import AudioQuestionGenerator
from django.db import DatabaseError
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from quiz_app.models import Quiz


class CreateQuizView(APIView):
    """
    Create a quiz from a YouTube video URL.

    Authenticated users can submit a YouTube URL to automatically 
    generate a quiz. The view handles multiple processing steps:
    - Downloads the audio from the YouTube video.
    - Transcribes the audio using Whisper.
    - Generates quiz questions using the Gemini model.
    - Cleans up and refines the generated text.
    - Deletes temporary transcription and generation files.

    Returns:
        - 201 Created: Successfully generated and saved the quiz.
        - 400 Bad Request: Validation errors in the submitted data.
        - 500 Internal Server Error: If any processing step (audio download, 
          transcription, question generation, or cleanup) fails.

    Requires JWT authentication and that the user is the resource owner.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]
    
    def post(self, request):
        serializer = YoutubeURLSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            url = serializer.validated_data['url']

            generate = AudioQuestionGenerator()
            try:
                generate.download_audio(url)
            except Exception as e:
                return Response({"detail": f"Audio download failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            try:
                generate.transcribe_whisper()
            except Exception as e:
                return Response({"detail": f"Whisper transcription failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            try:
                generate.generate_questions_gemini()
            except Exception as e:
                return Response({"detail": f"Generating questions with Gemini failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            try:
                generate.edge_cleaner_text()
            except Exception as e:
                return Response({"detail": f"Cleaning text ending failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            try:
                generate.delete_transcribed_text()
            except Exception as e:
                return Response({"detail": f"Deleting transcribed text failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
               
            try:
                quiz = serializer.create()
                return Response(CreateQuizSerializer(quiz).data, status=status.HTTP_201_CREATED)
            finally:
                generate.delete_generated_text()

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyQuizzesView(generics.ListAPIView):
    """
    Retrieve all quizzes created by the authenticated user.

    Returns a list of quizzes owned by the currently authenticated user.
    Each quiz includes serialized details such as title, questions, and 
    creation metadata.

    Returns:
        - 200 OK: Successfully retrieved the user's quizzes.
        - 500 Internal Server Error: If an unexpected error occurs while fetching data.

    Requires JWT authentication and ownership permissions.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request, *args, **kwargs):
        try:
            quiz = Quiz.objects.filter(owner=self.request.user)
            serializer = MyQuizzesSerializer(quiz, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
    
        except Exception as e:
            return Response({'detail': {str(e)}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class QuizSingleView(APIView):
    """
    Retrieve, update, or delete a quiz by its ID.

    Only the authenticated owner can access this endpoint.
    Requires JWT authentication.

    Responses:
        - 200 OK: Quiz retrieved or updated successfully.
        - 204 No Content: Quiz deleted successfully.
        - 400 Bad Request: Invalid data.
        - 401 Unauthorized / 403 Forbidden: Access denied.
        - 404 Not Found: Quiz not found.
        - 500 Internal Server Error: Unexpected error.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request, pk):
        try:
            quiz = get_object_or_404(Quiz, id=pk)
            serializer = MyQuizzesSerializer(quiz, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
    
        except Exception as e:
            return Response({'error': f'Unexpected error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def patch(self, request, pk):
        try:
            quiz = Quiz.objects.get(id=pk)
        except Quiz.DoesNotExist:
            return Response({"detail": "Quiz not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = QuizSinglePatchSerializer(quiz, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            quiz = serializer.save()
            return Response(MyQuizzesSerializer(quiz, context={'request': request}).data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        quiz = get_object_or_404(Quiz, id=pk)
        try:
            quiz.delete()
        except DatabaseError as e:
            return Response({'error': f'Unexpected error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=status.HTTP_204_NO_CONTENT)