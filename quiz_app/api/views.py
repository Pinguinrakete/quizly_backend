from .permissions import IsOwner
from .serializers import YoutubeURLSerializer, CreateQuizSerializer
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
    pass