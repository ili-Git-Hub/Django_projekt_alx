from .base import *


DEBUG = True
ALLOWED_HOSTS = ['*']   #dopuszczamy w dev wszystkie testowe srodowiska, /w prod beda doment

#bedzie sluzyl do podlaczenia sie jakiegos api do django, taki barier token:
#wygenerowany klucz z generator_klucza.py wklejamy tutaj
SECRET_KEY = 'd5pg-l16xj=)rs9eu@-=pjfin_9m-vg$e@9$=w+foy6ku29g+k'

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}