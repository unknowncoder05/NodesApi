import os
from os.path import join
from distutils.util import strtobool
import dj_database_url
from configurations import Configuration

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Common(Configuration):
    
    DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',


        # Third party apps
        'rest_framework',            # utilities for rest apis
        'django_filters',            # for filtering rest endpoints
        'corsheaders',

        # Your apps
        'api.users',
        'api.feed',
        'api.nodes',
    )

    # https://docs.djangoproject.com/en/2.0/topics/http/middleware/
    MIDDLEWARE = (
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
    )

    SESSION_COOKIE_HTTPONLY = True
    CSRF_COOKIE_HTTPONLY = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'

    ALLOWED_HOSTS = ["*"]
    ROOT_URLCONF = 'api.urls'
    SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
    WSGI_APPLICATION = 'api.wsgi.application'

    # Email
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

    ADMINS = (
        ('Author', 'yersonlasso05@gmail.com'),
    )

    # Postgres
    DATABASES = {
        'default': dj_database_url.config(
            default='postgres://postgres:@postgres:5432/postgres',
            conn_max_age=int(os.getenv('POSTGRES_CONN_MAX_AGE', 600))
        )
    }

    # General
    APPEND_SLASH = False
    TIME_ZONE = 'UTC'
    LANGUAGE_CODE = 'en-us'
    # If you set this to False, Django will make some optimizations so as not
    # to load the internationalization machinery.
    USE_I18N = False
    USE_L10N = True
    USE_TZ = True
    LOGIN_REDIRECT_URL = '/'

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/2.0/howto/static-files/
    STATIC_ROOT = os.path.normpath(join(os.path.dirname(BASE_DIR), 'static'))
    STATICFILES_DIRS = []
    STATIC_URL = '/static/'
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )

    # Media files
    MEDIA_ROOT = join(os.path.dirname(BASE_DIR), 'media')
    MEDIA_URL = '/media/'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': STATICFILES_DIRS,
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

    # Set DEBUG to False as a default for safety
    # https://docs.djangoproject.com/en/dev/ref/settings/#debug
    DEBUG = strtobool(os.getenv('DJANGO_DEBUG', 'no'))

    # Password Validation
    # https://docs.djangoproject.com/en/2.0/topics/auth/passwords/#module-django.contrib.auth.password_validation
    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]

    # Logging
    if False:
        LOGGING = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'django.server': {
                    '()': 'django.utils.log.ServerFormatter',
                    'format': '[%(server_time)s] %(message)s',
                },
                'verbose': {
                    'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
                },
                'simple': {
                    'format': '%(levelname)s %(message)s'
                },
            },
            'filters': {
                'require_debug_true': {
                    '()': 'django.utils.log.RequireDebugTrue',
                },
            },
            'handlers': {
                'django.server': {
                    'level': 'INFO',
                    'class': 'logging.StreamHandler',
                    'formatter': 'django.server',
                },
                'console': {
                    'level': 'DEBUG',
                    'class': 'logging.StreamHandler',
                    'formatter': 'simple'
                },
                'mail_admins': {
                    'level': 'ERROR',
                    'class': 'django.utils.log.AdminEmailHandler'
                }
            },
            'loggers': {
                'django': {
                    'handlers': ['console'],
                    'propagate': True,
                },
                'django.server': {
                    'handlers': ['django.server'],
                    'level': 'INFO',
                    'propagate': False,
                },
                'django.request': {
                    'handlers': ['mail_admins', 'console'],
                    'level': 'ERROR',
                    'propagate': False,
                },
                'django.db.backends': {
                    'handlers': ['console'],
                    'level': 'INFO'
                },
            }
        }

    # Custom user app
    AUTH_USER_MODEL = 'users.User'

    # Django Rest Framework
    REST_FRAMEWORK = {
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
        'PAGE_SIZE': int(os.getenv('DJANGO_PAGINATION_LIMIT', 12)),
        'DATETIME_FORMAT': '%Y-%m-%dT%H:%M:%S%z',
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
            'rest_framework.renderers.BrowsableAPIRenderer',
        ),
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'api.utils.auth0.validator.Auth0JWTBearerTokenAuthentication',
        ],
    }


    AUTH0_CLIENT_ID = os.environ.get('AUTH0_CLIENT_ID')
    AUTH0_CLIENT_SECRET = os.environ.get('AUTH0_CLIENT_SECRET')
    AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
    API_IDENTIFIER = os.environ.get('API_IDENTIFIER')

    DRF_PYJWT_KWARGS = {"audience": f"https://{AUTH0_DOMAIN}/api/v2/"}
    DRF_PYJWT_LOOKUP_USER = 'api.utils.auth0.user.lookup_user.lookup_user'

