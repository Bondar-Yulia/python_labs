import os
import django

# Налаштування середовища Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'car_dealership.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Перевірка наявності суперкористувача з цим ім'ям
if not User.objects.filter(username='Yulia').exists():
    User.objects.create_superuser('Yulia', 'yuliabondar18aaaa@gmail.com', '1234')
    print('Superuser created.')
else:
    print('Superuser already exists.')
