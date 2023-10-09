# Currencies

Бекенд сервиса для отслеживания динамики курса рубля.

## Запуск проекта

Клонировать репозиторий и перейти в него в командной строке:
```shell
git clone https://github.com/bochikas/currencies.git
```
```shell
cd currencies
```

Необходимо создать и заполнить файл .env переменными окружения(можно взять из файла .env.example):

```dotenv
POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_HOST
POSTGRES_PORT

SECRET_KEY
DEBUG

ALLOWED_HOSTS

REDIS_DB
REDIS_HOST
REDIS_PORT
```

Запустить docker-compose:
```shell
docker-compose up -d --build
```
Выполняем миграции:
```shell
docker-compose exec app python manage.py migrate --noinput
```
Создаем суперпользователя Django:
```shell
docker-compose exec app python manage.py createsuperuser
```
Останавливаем и удаляем контейнеры, сети, тома и образы:
```shell
docker-compose down -v
```

## Документация

Документация к API доступна по адресу:
```
http://127.0.0.1:8888/api/v1/docs/
```

### Flower

Таски celery можно посмотреть на странице
```
http://127.0.0.1:5555
```
