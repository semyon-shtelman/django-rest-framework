from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = 'Создает тестовых пользователей'

    def handle(self, *args, **options):
        users_count = User.objects.filter(is_superuser=False).count()
        User.objects.exclude(is_superuser=True).delete()
        self.stdout.write(f'{users_count}')

        users_data = [
            {'email': 'alice@example.com', 'password': 'testpass123'},
            {'email': 'bob@example.com', 'password': 'testpass123'},
            {'email': 'charlie@example.com', 'password': 'testpass123'},
            {'email': 'diana@example.com', 'password': 'testpass123'},
            {'email': 'eva@example.com', 'password': 'testpass123'},
        ]

        created = 0
        for user_data in users_data:
            user = User.objects.create(
                email=user_data['email'],
                password=user_data['password']
            )
            user.save()
            created += 1
            self.stdout.write(self.style.SUCCESS(f'Создан пользователь {user.email}'))
        self.stdout.write(self.style.SUCCESS(f'Готово! Создано {created} пользователей.'))
        self.stdout.write(self.style.SUCCESS('Доступные пользователи:'))
        for user in User.objects.filter(is_superuser=False):
            self.stdout.write(f'{user.email} - {user.password}')