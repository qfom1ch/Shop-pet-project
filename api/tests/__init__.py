import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')


django.setup()
