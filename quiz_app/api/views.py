from .permissions import IsOwner, HeaderOrCookieJWTAuthentication
from .serializers import YoutubeURLSerializer, CreateQuizSerializer, MyQuizzesSerializer, QuizSinglePatchSerializer
from .utils import AudioQuestionGenerator
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
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
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request, pk):
        try:
            quiz = Quiz.objects.get(id=pk)
        except Quiz.DoesNotExist:
            return Response({"detail": "Quiz not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CreateQuizSerializer(quiz, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


    def patch(self, request, pk):
        try:
            order = Quiz.objects.get(pk=pk)
        except Quiz.DoesNotExist:
            return Response({"detail": "Quiz not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = QuizSinglePatchSerializer(order, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            quiz = serializer.save()
            return Response(CreateQuizSerializer(quiz, context={'request': request}).data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        try:
            quiz = Quiz.objects.get(pk=id)
        except Quiz.DoesNotExist:
            return Response({"detail": "Quiz not found."}, status=status.HTTP_404_NOT_FOUND)       

        quiz.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


        #         serializer = OfferListSingleSerializer(offer, context={'request': request})
        #     return Response(serializer.data, status=status.HTTP_200_OK)
        # except Offer.DoesNotExist:
        #     return Response({'error': 'Offer not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        # except Exception as e:
        #     return Response({'error': f'Unexpected error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)