from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Course, Lesson
from .serializers import CourseSerializer, LessonListSerializer, LessonSerializer
from education.permissions import IsModer, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    PERMISSIONS = {
        "create": [IsAuthenticated, ~IsModer],
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated, IsOwner | IsModer],
        "update": [IsAuthenticated, IsOwner | IsModer],
        "partial_update": [IsAuthenticated, IsOwner | IsModer],
        "destroy": [IsAuthenticated, IsOwner],
    }

    def get_permissions(self):
        return [p() for p in self.PERMISSIONS.get(self.action, [IsAuthenticated])]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModer]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonListSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModer]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModer]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
