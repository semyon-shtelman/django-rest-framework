from rest_framework import serializers
from payments.models import Payment
from education.models import Course, Lesson


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class PaymentCreateSerializer(serializers.Serializer):

    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        required=False
    )
    lesson_id = serializers.PrimaryKeyRelatedField(
        queryset=Lesson.objects.all(),
        required=False
    )

    def validate(self, attrs):
        course = attrs.get('course_id')
        lesson = attrs.get('lesson_id')

        if course and lesson:
            raise serializers.ValidationError(
                'Нельзя оплатить одновременно курс и урок'
            )
        if not course and not lesson:
            raise serializers.ValidationError(
                'Нужно указать курс или урок'
            )
        return attrs