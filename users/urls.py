from django.urls import path

from .views import PaymentListAPIView
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path('payments/', PaymentListAPIView.as_view(), name='payment-list')
]