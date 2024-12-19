"""
Django settings for ecomm project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# DJANGO_SETTINGS_MODULE = 'admin_app.eshop.settings'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-n7+!kp5_0edbiii%gly(y0)od=b08_$e6g$gq)i$q6wf6iba_0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

# Application definition
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eshop.settings')

STRIPE_PUBLIC_KEY = 'pk_test_51PAzshDKiabUxBOTDA8MnvpvuIEFcwfPszOItpHhUMz3Xjb2BuDyJDCNDz9uWeEuvj6QDFXQ1Gzg7TA6sXylIMO400juUkc3Ov'
STRIPE_SECRET_KEY = 'sk_test_51PAzshDKiabUxBOTExbY3tjWi4Mf56qjIRiw5fjMdJmVrScAPRvVp8YwhuCh2KXS6qeyJCkFNpqMLCesklFVIPPW00H9YYYOcN'

REDIRECT_DOMAIN = "http://127.0.0.1:8000/api/home"

#AWS
AWS_ACCESS_KEY_ID = 'AKIA2UC3AUDUTZ6IV5NX'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'ecommshop'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_SIGNATURE_NAME = 's3v4'
AWS_S3_REGION_NAME = 'eu-central-1'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_VERITY = True
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'admin_app.app.apps.AdminServiceAppConfig',
    'storages',
]

CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = ['http://localhost:8000']  # Add your server IP/URL if needed
SESSION_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SECURE = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'eshop.urls'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

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

WSGI_APPLICATION = 'admin_app.eshop.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'admin-app',
        'USER': 'postgres',
        'PASSWORD': 'itB{V-~G>Zyq^]\R',
        'HOST': '34.118.110.89',
        'PORT': '5432',
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'admin-app-sql',
#         'USER': 'postgres',
#         'PASSWORD': 'itB{V-~G>Zyq^]\R',
#         'HOST': '/cloudsql/main_app-integration-435314:europe-central2:admin-app',
#         'PORT': '5432',
#     }
# }
# # }
# 'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'admin-app',
#         'USER': 'postgres',
#         'PASSWORD': 'ke{,I4JEe+tZFM33',
#         'HOST': '/cloudsql/main_app-integration-435314:europe-central2:page-app',
#         'PORT': '15432',
#     }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'admin_app', 'app', 'static')]
WHITENOISE_USE_FINDERS = True
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'app.User'

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True