DEBUG = False
DEBUG = True

ADMINS = (
    ('vamdc dictionary', 'thomas.marquart@astro.uu.se'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'dict.sqlite',
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
STATIC_URL = '/'
#STATIC_ROOT='/opt/VamdcDictionary/static'
ALLOWED_HOSTS=['*']
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

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
#    'django.contrib.staticfiles',
    'django.contrib.admin',
    'browse',
)
