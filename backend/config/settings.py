import os
import secrets

SECRET_KEY = secrets.token_urlsafe(48)
DEBUG = False
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
INSTALLED_APPS = ["simulacoes"]
if api_host := os.getenv("CONFERE_API_HOST"):
    ALLOWED_HOSTS.append(api_host)
CORS_ALLOWED_ORIGINS = list(filter(None, os.getenv("CONFERE_WEB_ORIGINS", "").split(",")))
CORS_URLS_REGEX = r"^/api/"
CORS_ALLOWED_ORIGINS = [origin.strip() for origin in CORS_ALLOWED_ORIGINS]
ROOT_URLCONF = "config.urls"
MIDDLEWARE = ["corsheaders.middleware.CorsMiddleware", "django.middleware.security.SecurityMiddleware", "django.middleware.common.CommonMiddleware"]
DATA_UPLOAD_MAX_MEMORY_SIZE = 16384
USE_TZ = True
