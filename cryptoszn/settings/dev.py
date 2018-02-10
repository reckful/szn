from __future__ import absolute_import, unicode_literals

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5q35)sa8^)a+*7*i-=#nzdnzyg6-g3^uhm_c^!1q!60^a*pr0n'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ALLOWED_HOSTS = ['cryptoszn-obdnc.c9users.io']
STATIC_ROOT = os.path.join(BASE_DIR, "static")

try:
    from .local import *
except ImportError:
    pass
