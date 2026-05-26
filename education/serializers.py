from rest_framework import serializers
from .models import Course, Lesson, Subscription
from .validators import validate_links

class LessonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'title', 'preview')

class LessonSerializer(serializers.ModelSerializer):
    content = serializers.CharField(
        validators=[validate_links]
    )
    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ('owner', 'created_at')


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonListSerializer(many=True, read_only=True)
    description = serializers.CharField(
        validators=[validate_links]
    )
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Subscription.objects.filter(
            user=user,
            course=obj
        ).exists()

    def get_lesson_count(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = ('id', 'is_subscribed', 'title', 'description', 'preview', 'lesson_count', 'lessons',)
        read_only_fields = ('owner', 'created_at')
