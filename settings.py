import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent


def _read_secrets():
    """secrets.txt sits next to this file, KEY=value per line. See secrets.txt.example."""
    secrets = {}
    try:
        lines = (BASE_DIR / 'secrets.txt').read_text().splitlines()
    except FileNotFoundError:
        return secrets
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        key, sep, value = line.partition('=')
        if sep:
            secrets[key.strip()] = value.strip().strip('\'"')
    return secrets


SECRETS = _read_secrets()


def setting(name, default=''):
    """Environment wins over secrets.txt, so a deployment can override either way."""
    return os.environ.get(name) or SECRETS.get(name, default)


DEBUG = setting('VAMDC_DICT_DEBUG') == '1'

SECRET_KEY = setting('VAMDC_DICT_SECRET_KEY')
if not SECRET_KEY:
    if not DEBUG:
        raise ImproperlyConfigured(
            'No VAMDC_DICT_SECRET_KEY in the environment or in %s'
            % (BASE_DIR / 'secrets.txt'))
    SECRET_KEY = 'insecure-key-for-local-development-only'

ADMINS = (
    ('vamdc dictionary', 'thomas.marquart@physics.uu.se'),
)

SERVER_EMAIL = 'vamdc-dict-noreply@neon.physics.uu.se'
DEFAULT_FROM_EMAIL = SERVER_EMAIL

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'dict.sqlite',
    }
}
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
TIME_ZONE = 'Europe/Stockholm'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
USE_TZ = True

ROOT_URLCONF = 'urls'
APPEND_SLASH = True
# /new/ posts one id plus one checkbox per dictionary keyword, well past the
# default limit of 1000
DATA_UPLOAD_MAX_NUMBER_FIELDS = 5000
ALLOWED_HOSTS = setting('VAMDC_DICT_HOSTS', '*').split(',')

# Django >= 4 checks the Origin header on POST, so the admin login needs the
# public https origin listed here. Caddy redirects the .org name to .eu, so .eu
# is what browsers actually post from.
CSRF_TRUSTED_ORIGINS = setting('VAMDC_DICT_ORIGINS', 'https://dictionary.vamdc.eu').split(',')
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# the admin is the only write surface, so keep its session off plain http.
# TLS itself (redirect, HSTS) is Caddy's job.
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'browse',
)
