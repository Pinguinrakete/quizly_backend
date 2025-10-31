from .permissions import IsOwner
from .serializers import YoutubeURLSerializer, CreateQuizSerializer
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from quiz_app.models import Quiz


class CreateQuizView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    def post(self, request):
        serializer = YoutubeURLSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                quiz = serializer.save()
                return Response(CreateQuizSerializer(quiz).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyQuizzesView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = CreateQuizSerializer

    def get_queryset(self):
        return Quiz.objects.filter(owner=self.request.user)


class QuizSingleView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    def delete(self, request, id):
        try:
            quiz = Quiz.objects.get(pk=id)
        except Quiz.DoesNotExist:
            return Response({"detail": "Quiz not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if request.user.id != quiz.owner.id:
            return Response({"detail": "Only the owner can delete this quiz."}, status=status.HTTP_403_FORBIDDEN)

        quiz.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    