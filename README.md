Данный проект представляет собой сервис рассылки уведомлений.

Django REST, Sqlite3, Celery, Redis, (Django AllAuth в процессе)

Проект разработан на основе фреймворка Django REST, используемая БД SQLite, мониторинг задач реализован с помощью Celery.

<h3>Задача</h3>

Необходимо разработать сервис управления рассылками API администрирования и получения статистики.

Описание

Необходимо реализовать методы создания новой рассылки, просмотра созданных и получения статистики по выполненным рассылкам.
Реализовать сам сервис отправки уведомлений на внешнее API.

Приложение содержит следущие роуты:
- /admin/ -панель администратора
- /docs/ - Swagger документация
- /api/v1/ - API
- /openapi/ - OpenApi схема

Чтобы скопировать проект и запустить его у себя:

1. Создайте виртуальное окружение в папке, куда планируете скачать проект: python -m venv
(например, python -m venv C:\Users\project)

2. Активируйте виртуальное окружение командой Scripts\activate.bat

3. Скачайте проект по ссылке https://github.com/iren-coder/Test_project_Django_REST_Mailing_API либо склонируйте репозиторий git@github.com:iren-coder/Test_project_Django_REST_Mailing_API.git.

4. Установите требуемые зависимости: 
    pip install -r requirements.txt

5. Создайте суперпользователя python manage.py createsuperuser

6. Создайте и примините миграции:
python manage.py makemigrations
python manage.py migrate

7. Поместите в корневую папку с проектом файл .env

   Структура файла .env:
    PROBE_SERVER_URL=https://probe.fbrq.cloud/v1/send/

    PROBE_SERVER_TOKEN=very_secret_token

    SECRET_KEY=django_secret_key

    DEBUG=TRUE

8. Теперь можно запустить сервер python manage.py runserver

9. Запустить мониторинг задач Celery:
   celery worker
   flower -A app --port=5555
   Мониторинг задач Celery (Flower) осуществляется по адресу: http://127.0.0.1:5555/
