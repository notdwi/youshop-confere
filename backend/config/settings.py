import secrets

SECRET_KEY = secrets.token_urlsafe(48)
DEBUG = False
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
INSTALLED_APPS = ["simulacoes"]
ROOT_URLCONF = "config.urls"
MIDDLEWARE = ["django.middleware.security.SecurityMiddleware", "django.middleware.common.CommonMiddleware"]
DATA_UPLOAD_MAX_MEMORY_SIZE = 16384
USE_TZ = True
