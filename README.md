# Тестовое задание
## Цель: реализовать сервер загрузки текстовых файлов на локальный диск

## Запуск проекта:

**Клонируйте репозиторий командой:**

```git clone https://github.com/EvgenyCh97/test_task.git```

**Перейдите в каталог с проектом:**

```cd test_task```

**Установите виртуальное окружение, чтобы изолировать зависимости проекта:**

```python -m venv env```

**Активируйте виртуальное окружение:**

На Windows: ```env\Scripts\activate```

На MacOS/Linux: ```source env/bin/activate```

**Установите зависимости проекта:**

```pip install -r requirements.txt```

**Примените миграции к базе данных**

```python manage.py migrate```

**Создайте директорию ```media``` в корне проекта и файл ```.env``` со следующим содержимым:**

DEBUG=True

SECRET_KEY='<*ваш_секретный_ключ*>'

**Запустите проект:**

```python manage.py runserver```

**Пройдите по URL-адресу http://127.0.0.1:8000/ для проверки работоспособности сервера**