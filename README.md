# Django + restapi

## Установка проекта

### Создать базу postgresql
```
Название базы: djangoproject
Далее применяем миграции: python manage.py migrate
```

### Устанавливаем зависимости
```
pip install -r requirements.txt
```

### Запуск проекта
```
python manage.py runserver
```

### В проекте
```
Список пользователей /api/users/ (для примера)
Настройки:
Serializers - core.serializers
Views - core.views
Models - core.views
Routers - _project_.routers
```
