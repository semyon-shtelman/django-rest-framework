# Платформа для онлайн-обучения
Учебный Django-проект для онлайн-обучения с курсами, платежами и фоновыми задачами.

## Добавлен CI/CD Pipeline и Docker-развертывание

### Описание
В этом PR реализован полный CI/CD пайплайн для автоматического тестирования, сборки и деплоя проекта на удаленный сервер.

#### Настройка CI/CD (GitHub Actions)
- Добавлен workflow `.github/workflows/deploy.yml`
- Этап **Линтинг**: flake8, black, isort
- Этап **Тесты**: запуск тестов Django с PostgreSQL
- Этап **Билд**: сборка Docker образа и пуш в GitHub Container Registry
- Этап **Деплой**: автоматическое развертывание на сервер

#### Docker-контейнеризация
- Добавлен `Dockerfile` для Django приложения
- Добавлен `docker-compose.yml` со всеми сервисами:
  - PostgreSQL (база данных)
  - Redis (брокер для Celery)
  - Django (веб-приложение)
  - Celery Worker (фоновые задачи)
  - Celery Beat (планировщик)
  - Nginx (reverse proxy)

### Secrets для деплоя
Для работы деплоя необходимо добавить следующие секреты в GitHub:

### Secret Описание 

- `SERVER_SSH_KEY`: Приватный SSH-ключ для доступа к серверу |
- `SERVER_HOST`:IP-адрес сервера |
- `SSH_USER`: Имя пользователя на сервере |
- `DEPLOY_DIR`:Путь к проекту на сервере |
- `DB_NAME`: Имя базы данных |
- `DB_USER`: Пользователь базы данных |
- `DB_PASSWORD`: Пароль базы данных |
- `SECRET_KEY`: Django SECRET_KEY |
- `ADMIN_PASSWORD`: Пароль суперпользователя |

```bash
# Клонировать репозиторий
git clone <https://github.com/semyon-shtelman/django-rest-framework.git>
```

# Создать .env файл
cp .env.example .env
### Инструкция по деплою

#### Автоматический деплой
1. Смержить PR в ветку `main`
2. GitHub Actions автоматически запустит деплой
3. Приложение будет доступно по адресу: `http://<SERVER_HOST>`

#### Ручной деплой (на сервере)
```bash
git clone <https://github.com/semyon-shtelman/django-rest-framework.git>
cd ~/django-rest-framework
git pull origin main
docker compose up -d --build
```