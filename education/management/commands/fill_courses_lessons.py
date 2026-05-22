from django.core.management.base import BaseCommand
from courses.models import Course, Lesson


class Command(BaseCommand):
    help = 'Создает тестовые курсы и уроки для разработки'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Очищаю существующие данные...'))
        lessons_count = Lesson.objects.count()
        Lesson.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Удалено уроков: {lessons_count}'))

        courses_count = Course.objects.count()
        Course.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Удалено курсов: {courses_count}'))

        self.stdout.write(self.style.SUCCESS('Начинаю создание тестовых данных...'))

        courses_data = [
            {
                'title': 'Django для начинающих',
                'description': 'Полный курс по Django с нуля. Изучите основы веб-разработки.',
            },
            {
                'title': 'Django REST Framework (DRF)',
                'description': 'Создание мощных API для ваших проектов. REST, сериализаторы, авторизация.',
            },
            {
                'title': 'React + Django интеграция',
                'description': 'Научитесь связывать популярный фронтенд с Django бэкендом.',
            },
            {
                'title': 'Асинхронный Django с Channels',
                'description': 'Создайте WebSocket приложения: чаты, онлайн-игры, уведомления.',
            },
            {
                'title': 'Деплой Django проектов',
                'description': 'Настройка Docker, PostgreSQL, Nginx и деплой на сервер.',
            },
        ]

        created_courses = []
        for course_data in courses_data:
            course = Course.objects.create(
                title=course_data['title'],
                description=course_data['description'],

            )
            created_courses.append(course)

            self.stdout.write(self.style.SUCCESS(f'Создан курс: {course.title}'))

        lessons_data = {
            'Django для начинающих': [
                {'title': 'Введение в Django', 'content': 'Установка, создание первого проекта, структура папок.'},
                {'title': 'Модели и базы данных', 'content': 'ORM, миграции, работа с PostgreSQL.'},
                {'title': 'Контроллеры и маршруты', 'content': 'Создание views, настройка urlpatterns.'},
                {'title': 'Шаблоны и статика', 'content': 'Django Templating Engine, CSS, JS подключение.'},
                {'title': 'Формы и валидация', 'content': 'Создание форм, обработка данных пользователя.'},
            ],
            'Django REST Framework (DRF)': [
                {'title': 'Что такое REST API?', 'content': 'Принципы REST, архитектура API.'},
                {'title': 'Сериализаторы', 'content': 'ModelSerializer, валидация, вложенные данные.'},
                {'title': 'ViewSets и роутеры', 'content': 'ModelViewSet, DefaultRouter, кастомные действия.'},
                {'title': 'Аутентификация и права', 'content': 'TokenAuthentication, JWT, permission classes.'},
                {'title': 'Фильтрация и пагинация', 'content': 'Filtering, sorting, pagination.'},
            ],
            'React + Django интеграция': [
                {'title': 'Настройка проекта', 'content': 'Django + React в одном проекте.'},
                {'title': 'API подключение', 'content': 'Axios, fetch, CORS настройка.'},
                {'title': 'Состояние приложения', 'content': 'Redux, контекст, работа с данными.'},
            ],
            'Асинхронный Django с Channels': [
                {'title': 'WebSocket основы', 'content': 'Отличие от HTTP, установка Channels.'},
                {'title': 'Создание чата', 'content': 'Комнаты, уведомления, broadcasting.'},
            ],
            'Деплой Django проектов': [
                {'title': 'Docker контейнеризация', 'content': 'Dockerfile, docker-compose.'},
                {'title': 'Настройка Nginx', 'content': 'Проксирование, статика, media.'},
                {'title': 'Деплой на сервер', 'content': 'DigitalOcean, AWS, GitHub Actions.'},
            ],
        }

        created_lessons = []
        for course in created_courses:
            if course.title in lessons_data:
                for lesson_data in lessons_data[course.title]:
                    lesson = Lesson.objects.create(
                        course=course,
                        title=lesson_data['title'],
                        content=lesson_data['content']
                    )
                    created_lessons.append(lesson)
                    self.stdout.write(
                            self.style.SUCCESS(f'Создан урок: {lesson.title} курс: {course.title})'))

        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS(f'ГОТОВО! Создано курсов: {len(created_courses)}'))
        self.stdout.write(self.style.SUCCESS(f'Создано уроков: {len(created_lessons)}'))
        self.stdout.write(self.style.SUCCESS('=' * 50))

        self.stdout.write(self.style.SUCCESS('Содержимое базы данных:'))
        for course in Course.objects.all():
            lessons_count = course.lessons.count()
            self.stdout.write(f'{course.title} — уроков: {lessons_count}')
            for lesson in course.lessons.all():
                self.stdout.write(f'{lesson.title}')