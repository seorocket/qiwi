# Django + restapi

### Установка создаем виртуальное окружение
```
virtualenv -p python3 .venv
```

### Устанавливаем зависимости
```
pip install -r requirements.txt
```

### Создать базу postgresql
```
Название базы: qiwi
Далее применяем миграции: python manage.py migrate
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
Models - core.models
Routers - _project_.routers
```
