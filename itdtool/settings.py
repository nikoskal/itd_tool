"""
Django settings for sped project.
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

settings_dir = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.dirname(settings_dir))
CONFFILES_FOLDER = os.path.join(PROJECT_ROOT, 'conf_files/')



# read the security parameters from external file named "security_params.conf"
sec_params = {}
try:
    with open("security_params.conf") as f:
        for line in f:
            (key, val) = line.split()
            sec_params[str(key)] = val
except IOError:
    print 'Cannot open file: security_params.conf'
    print 'Make sure that security_params.conf file exists in the same folder as manage.py'

SECRET_KEY = sec_params['SECRET_KEY']



DB_NAME = sec_params['DB_NAME']
DB_ENGINE = sec_params['DB_ENGINE']
DB_USER = sec_params['DB_USER']
DB_PASSWORD = sec_params['DB_PASSWORD']
DB_HOST = sec_params['DB_HOST']
DB_PORT = sec_params['DB_PORT']

# GOOGLE TRENDS Security parameters
GOOGLE_USERNAME = sec_params['GOOGLE_USERNAME']
GOOGLE_PASSWORD = sec_params['GOOGLE_PASSWORD']

# TWITTER TRENDS Security parameters
TWITTER_KEY = sec_params['TWITTER_KEY']
TWITTER_SECRET = sec_params['TWITTER_SECRET']
TWITTER_ACCESS_TOKEN = sec_params['TWITTER_ACCESS_TOKEN']
TWITTER_ACCESS_TOKEN_SECRET = sec_params['TWITTER_ACCESS_TOKEN_SECRET']

# ADWORDS Security parameters
ADWORDS_USERNAME = sec_params['ADWORDS_USERNAME']
ADWORDS_PASSWORD = sec_params['ADWORDS_PASSWORD']

# GENDERIZE_API_KEY
GENDERIZE_API_KEY = sec_params['GENDERIZE_API_KEY']

# FACE PP
FACE_API_KEY = sec_params['FACE_API_KEY']
FACE_API_SECRET = sec_params['FACE_API_SECRET']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

X_FRAME_OPTIONS = 'DENY'
CSRF_COOKIE_HTTPONLY = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_SSL_REDIRECT = True
# when DEBUG = False set ALLOWED_HOSTS
# ALLOWED_HOSTS = ['debfed.lab.netmode.ece.ntua.gr','127.0.0.1']

# render jinja template
# TEMPLATE_DEBUG = False

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'itdtool',
    'corsheaders',
    'rest_framework.authtoken',
    # 'raven.contrib.django.raven_compat',

)



MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

CSRF_COOKIE_SECURE = True

ROOT_URLCONF = 'itdtool.urls'

WSGI_APPLICATION = 'itdtool.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': DB_ENGINE,
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CORS_ORIGIN_ALLOW_ALL = True

# RabbitMQ: Broker settings.
BROKER_URL = 'amqp://guest:guest@localhost//'

# CELERY: List of modules to import when celery starts.
CELERY_IMPORTS = ('itdtool.tasks.query_params_task', 'itdtool.tasks.gtrends_task','itdtool.tasks.twitter_task',
                                                                                  'itdtool.tasks.adwords_task',
                  'itdtool.tasks.history_task')

# REDIS: Using the database to store task state and results.
CELERY_RESULT_BACKEND = 'redis://'

# Sentry: logging
# RAVEN_CONFIG = {
#     'dsn': 'https://477b70b331cd472e921a9cc6a39a2dc8:1a7b3e6861fe486ca5b86434cc01e2f0@app.getsentry.com/66620'
# }

# REST_FRAMEWORK = {
#
#     'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination'
# }

# set the client IPs that the ITD service will accept calls
# if '0.0.0.0' is in list there are no restrictions.
ALLOWED_IP = ['0.0.0.0', '127.0.0.1']

STATIC_URL = '/static/'

