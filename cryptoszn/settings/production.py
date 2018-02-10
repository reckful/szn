from __future__ import absolute_import, unicode_literals

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5q35)sa8^)a+*7*i-=#nzdnzyg6-g3^uhm_c^!1q!60^a*pr0n'


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ALLOWED_HOSTS = ['www.cryptoszn.com']
SECURE_SSL_REDIRECT = True
STATIC_ROOT = os.path.join(BASE_DIR, "static")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pirrie$dbszn',
        'USER': 'pirrie',
        'PASSWORD': 'lewisisgay123',
        'HOST': 'pirrie.mysql.pythonanywhere-services.com',
    }
}

try:
    from .local import *
except ImportError:
    pass
