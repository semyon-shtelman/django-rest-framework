# Платформа для онлайн-обучения

Учебный проект на **Django REST Framework** для онлайн-обучения с курсами, уроками, платежами и фоновыми задачами.

## Стек технологий

* Python 3.12
* Django
* Django REST Framework
* PostgreSQL
* Redis
* Celery
* Celery Beat
* Gunicorn
* Nginx
* Docker
* Docker Compose
* GitHub Actions (CI/CD)

---

# Возможности проекта

* Регистрация и аутентификация пользователей
* CRUD для курсов и уроков
* Платежи
* Фоновые задачи с использованием Celery
* Периодические задачи Celery Beat
* PostgreSQL в качестве основной базы данных
* Redis как брокер сообщений
* Docker-контейнеризация
* Автоматический деплой через GitHub Actions

---

# CI/CD Pipeline

Проект использует GitHub Actions.

После каждого `push` в ветку `main` автоматически выполняются:

1. Проверка форматирования кода

   * Black
   * isort
   * flake8

2. Запуск тестов

3. Сборка Docker-образа

4. Публикация образа в Docker Hub

5. Автоматический деплой на удаленный сервер

Во время деплоя GitHub Actions:

* подключается к серверу по SSH;
* копирует `docker-compose.prod.yml`;
* копирует `nginx.conf`;
* скачивает актуальный Docker-образ;
* запускает контейнеры;
* выполняет миграции;
* собирает статические файлы.

---

# Структура Docker

Проект использует два Compose-файла.

## docker-compose.yml

Используется для локальной разработки.

Особенности:

* сборка приложения через `build`;
* автоматическая синхронизация исходного кода;
* запуск Django Development Server.

---

## docker-compose.prod.yml

Используется только на сервере.

Особенности:

* приложение запускается из готового Docker-образа;
* используется Gunicorn;
* отсутствует синхронизация исходного кода;
* предназначен для production.

---

# Локальный запуск

## 1. Клонировать репозиторий

```bash
git clone https://github.com/semyon-shtelman/django-rest-framework.git

cd django-rest-framework
```

---

## 2. Создать файл `.env`

Скопируйте шаблон

```bash
cp .env.example .env
```

Заполните необходимые переменные окружения.

---

## 3. Запустить контейнеры

```bash
docker compose up --build
```

При первом запуске будут автоматически:

* собраны Docker-образы;
* применены миграции;
* запущены все сервисы.

---

## Локально будут запущены

* Django
* PostgreSQL
* Redis
* Celery Worker
* Celery Beat
* Nginx

---

## Остановка проекта

```bash
docker compose down
```

Для удаления томов:

```bash
docker compose down -v
```

---

# Первоначальная настройка сервера

Перед первым запуском GitHub Actions необходимо подготовить сервер.

---

## 1. Подключитесь к серверу

```bash
ssh <user>@<server_ip>
```

---

## 2. Создайте директорию проекта

```bash
sudo mkdir -p /opt/django-rest-framework
```

или

```bash
mkdir -p /opt/django-rest-framework
```

---

## 3. Перейдите в директорию проекта

```bash
cd /opt/django-rest-framework
```

---

## 4. Создайте файл `.env`

```bash
nano .env
```

Скопируйте содержимое файла `.env.example` из репозитория и заполните необходимые значения.

Сохраните файл.

---

## 5. Установите Docker и Docker Compose

Проверьте, что доступны команды:

```bash
docker --version
docker compose version
```

---

## 6. Настройте GitHub Secrets

В разделе **Settings → Secrets and variables → Actions** создайте следующие секреты:

### Docker Hub

* `DOCKER_HUB_USERNAME`
* `DOCKER_HUB_ACCESS_TOKEN`

### Сервер

* `SERVER_IP`
* `SSH_USER`
* `SERVER_SSH_KEY`

---

## 7. Выполните push в ветку `main`

```bash
git push origin main
```

GitHub Actions автоматически:

* выполнит линтинг;
* запустит тесты;
* соберет Docker-образ;
* загрузит его в Docker Hub;
* подключится к серверу;
* обновит конфигурационные файлы;
* скачает новую версию образа;
* выполнит миграции;
* соберет статические файлы;
* перезапустит контейнеры.

После завершения workflow приложение будет доступно по IP-адресу сервера.

---

# Используемые сервисы

| Сервис         | Назначение               |
| -------------- | ------------------------ |
| Django         | REST API                 |
| PostgreSQL     | База данных              |
| Redis          | Брокер сообщений         |
| Celery         | Выполнение фоновых задач |
| Celery Beat    | Планировщик задач        |
| Gunicorn       | WSGI-сервер              |
| Nginx          | Reverse Proxy            |
| Docker         | Контейнеризация          |
| GitHub Actions | CI/CD                    |

---

## API документация

После запуска проекта документация API доступна по следующим адресам:

### Swagger UI

```text
http://localhost/swagger/
```

или после деплоя

```text
http://<SERVER_IP>/swagger/
```

---

### ReDoc

```text
http://localhost/redoc/
```

или после деплоя

```text
http://<SERVER_IP>/redoc/
```

Документация генерируется автоматически на основе Django REST Framework и позволяет:

* просматривать доступные эндпоинты;
* изучать параметры запросов;
* тестировать API непосредственно из браузера;
* просматривать схемы запросов и ответов.
