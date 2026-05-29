from django.urls import path

from payments import views
from payments.apps import PaymentsConfig

app_name = PaymentsConfig.name

urlpatterns = [
    path('list/', views.PaymentListAPIView.as_view(), name='list-payments')
]