from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from config.settings import DEFAULT_FROM_EMAIL
from users.models import User


@shared_task
def send_course_update_email(course_title, emails):
    send_mail(
        subject="Обновление курса",
        message=f'Курс "{course_title}" был обновлён',
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=emails,
        fail_silently=False,
    )


@shared_task
def deactivate_inactive_users(days_inactive=30):
    month_ago = timezone.now() - timedelta(days=days_inactive)

    inactive_users = User.objects.filter(is_active=True, last_login__lt=month_ago)

    for user in inactive_users:
        send_mail(
            subject="Ваш аккаунт заблокирован за не активность",
            message=(
                f"Здравствуйте {user.email}"
                f"Ваш аккаунт был заблокирован, так как вы не заходили более месяца."
                f"Для разблокировки обратитесь в поддержку."
            ),
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        user.is_active = False
        user.save()
