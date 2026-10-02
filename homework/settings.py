import os
import ast
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def get_env_variable(var_name, required=False):
    """
    Fetch environment variable and optionally validate it exists.
    Returns None if not required and missing.
    """
    value = os.environ.get(var_name)
    if required and value is None:
        print(f"Error: Required environment variable '{var_name}' is not set.")
        sys.exit(1)
    return value

# Define required environment variables
REQUIRED_ENV_VARS = [
    'DEBUG',
    'ALLOWED_HOSTS',
    'CSRF_TRUSTED_ORIGINS',
    'DATABASE_NAME',
    'DATABASE_USER',
    'DATABASE_PASSWORD',
    'DATABASE_HOST',
    'DATABASE_PORT',
]

# Validate all required variables exist
for var in REQUIRED_ENV_VARS:
    get_env_variable(var, required=True)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-g(rs@h+jmvajn4b3qge)sz4gm12l0ypul%t)@o)_pxnytehenf'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_env_variable("DEBUG", required=True)
ALLOWED_HOSTS = ast.literal_eval(get_env_variable("ALLOWED_HOSTS", required=True))
CSRF_TRUSTED_ORIGINS = ast.literal_eval(get_env_variable("CSRF_TRUSTED_ORIGINS", required=True))

# Application definition

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'homework',
    'account',
    'chat',
]

# chat config
ASGI_APPLICATION = 'homework.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'homework.urls'

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

WSGI_APPLICATION = 'homework.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_env_variable("DATABASE_NAME", required=True),
        'USER': get_env_variable("DATABASE_USER", required=True),
        'PASSWORD': get_env_variable("DATABASE_PASSWORD", required=True),
        'HOST': get_env_variable("DATABASE_HOST", required=True),
        'PORT': get_env_variable("DATABASE_PORT", required=True),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'account.UserAccount'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STRIPE_PUBLISHABLE_KEY = get_env_variable("publishable_key", required=False)
STRIPE_SECRET_KEY = get_env_variable("secret_key", required=False)
