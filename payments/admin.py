from django.contrib import admin

from payments.models import Payment


@admin.register(Payment)
class AdminPayment(admin.ModelAdmin):
    list_display = ("id", "user", "amount")
