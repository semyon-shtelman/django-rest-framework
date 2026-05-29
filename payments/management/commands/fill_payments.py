from django.core.management.base import BaseCommand
from payments.models import Payment
from users.models import User
from education.models import Course, Lesson
import random

class Command(BaseCommand):
    help = 'Создает тестовые платежи'

    def handle(self, *args, **options):
        users = list(User.objects.filter(is_superuser=False))
        courses = list(Course.objects.all())
        lessons = list(Lesson.objects.all())

        if not users:
            self.stdout.write(self.style.ERROR('Ошибка: Нет пользователей.'))
            self.stdout.write('Запусти: python manage.py fill_users')
            return

        if not courses and not lessons:
            self.stdout.write(self.style.ERROR('Ошибка: Нет курсов и уроков.'))
            self.stdout.write('Запусти: python manage.py fill_courses_lessons')
            return

        payment_count = Payment.objects.count()
        Payment.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Очистка старых платежи ({payment_count} шт.)'))

        created = 0

        for course in courses:
            user = random.choice(users)
            Payment.objects.create(
                user=user,
                course=course,
                lesson=None,
                amount=4990,
                method='transfer'
            )
            created += 1
            self.stdout.write(f'{user.email} оплатил курс: {course.title}')

        for lesson in lessons:
            user = random.choice(users)
            Payment.objects.create(
                user=user,
                course=None,
                lesson=lesson,
                amount=990,
                method='cash'
            )
            created += 1
            self.stdout.write(f'{user.email} оплатил урок: {lesson.title}')

        # Итог
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'Готово! Создано {created} платежей.'))