from .settings import *

# Test settings
DEBUG = False
TEMPLATE_DEBUG = False

# Use in-memory SQLite database for testing
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Use console email backend for testing
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Use in-memory cache for testing
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Celery settings for testing
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# Media settings for testing
MEDIA_ROOT = BASE_DIR / 'test_media'
MEDIA_URL = '/media/'

# Static files settings for testing
STATIC_ROOT = BASE_DIR / 'test_static'
STATIC_URL = '/static/'

# Password hashers for faster testing
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Disable migrations for testing
class DisableMigrations:
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None

MIGRATION_MODULES = DisableMigrations()

# Disable logging during tests
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'null': {
            'class': 'logging.NullHandler',
        },
    },
    'root': {
        'handlers': ['null'],
        'level': 'CRITICAL',
    },
}

# Test-specific middleware
MIDDLEWARE = [
    middleware for middleware in MIDDLEWARE
    if middleware not in [
        'django.middleware.csrf.CsrfViewMiddleware',
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]
]

# Test-specific installed apps
INSTALLED_APPS = [
    app for app in INSTALLED_APPS
    if app not in [
        'debug_toolbar',
        'django.contrib.admin',
        'django.contrib.admindocs',
    ]
]

# Security settings for testing
ALLOWED_HOSTS = ['*']
SECRET_KEY = 'test-key-not-for-production'
DEBUG = False

# File upload settings for testing
FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
]
FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440  # 2.5 MB

# Authentication settings for testing
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# REST Framework settings for testing
REST_FRAMEWORK = {
    **REST_FRAMEWORK,
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'TEST_REQUEST_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'UNAUTHENTICATED_USER': None,
}

# JWT settings for testing
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# Celery settings for testing
CELERY_BROKER_URL = 'memory://'
CELERY_RESULT_BACKEND = 'cache+memory://'

# Test-specific settings
TEST_RUNNER = 'django.test.runner.DiscoverRunner'
TEST_NON_SERIALIZED_APPS = []

# Disable password validation during tests
AUTH_PASSWORD_VALIDATORS = []

# Disable timezone support during tests
USE_TZ = False

# Test-specific custom settings
TESTING = True
TEST_MODE = True

# Disable SSL during tests
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Disable rate limiting during tests
REST_FRAMEWORK['DEFAULT_THROTTLE_CLASSES'] = []
REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'] = {}