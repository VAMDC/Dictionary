DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('VALD user', 'vald@localhost'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/opt/VamdcDictionary/dict.sqlite',
    }
}

TEMPLATE_DIRS = (
    '/opt/VamdcDictionary/static/templates',
)

TIME_ZONE = 'Europe/Stockholm'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
USE_L10N = False
MEDIA_ROOT = ''
MEDIA_URL = ''
SECRET_KEY = '%l%4o(43#bv8&$7j=9!+%k+!vkpf*kg3@62js983'
ROOT_URLCONF = 'urls'
STATIC_URL = '/static/'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
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
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'browse',
)
