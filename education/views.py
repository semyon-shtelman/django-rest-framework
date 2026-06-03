from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from education.paginators import CustomPagination
from education.permissions import IsModer, IsOwner

from .models import Course, Lesson, Subscription
from .serializers import (CourseSerializer, LessonListSerializer,
                          LessonSerializer)

from .tasks import send_course_update_email

class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        course_item = get_object_or_404(Course, pk=pk)
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "подписка добавлена"
        return Response({"message": message})


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CustomPagination
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
        serializer.save(
            owner=self.request.user
        )

    def perform_update(self, serializer):
        course = serializer.save()

        subscriptions = Subscription.objects.filter(
            course=course
        )

        emails = list(
            subscriptions.values_list(
                'user__email',
                flat=True
            )
        )

        if emails:
            send_course_update_email.delay(
                course.title,
                emails
            )


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModer]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonListSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination


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
