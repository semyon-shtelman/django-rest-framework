from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import PaymentSerializer
from .models import Payment

class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['course', 'lesson', 'method']
    search_fields = ['course__title', 'lesson__title']
    ordering_fields = ['date', 'amount']
    ordering = ['-date']