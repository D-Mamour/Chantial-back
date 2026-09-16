"""Configuration principale du backend Chantial."""
import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
ALLOWED_HOSTS = [x.strip() for x in os.getenv("ALLOWED_HOSTS","127.0.0.1,localhost").split(",")]

INSTALLED_APPS = [
    "django.contrib.admin","django.contrib.auth","django.contrib.contenttypes",
    "django.contrib.sessions","django.contrib.messages","django.contrib.staticfiles",
    "rest_framework","rest_framework_simplejwt","corsheaders","drf_spectacular",
    "comptes","projets","finances","documents","intelligence","interactions","audit",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "config.urls"
TEMPLATES = [{
    "BACKEND":"django.template.backends.django.DjangoTemplates","DIRS":[],
    "APP_DIRS":True,
    "OPTIONS":{"context_processors":[
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
    ]},
}]
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

DATABASES = {"default":{
    "ENGINE":"django.db.backends.postgresql",
    "NAME":os.getenv("DB_NAME","chantial"),
    "USER":os.getenv("DB_USER","chantial"),
    "PASSWORD":os.getenv("DB_PASSWORD","chantial"),
    "HOST":os.getenv("DB_HOST","localhost"),
    "PORT":os.getenv("DB_PORT","5432"),
}}
AUTH_USER_MODEL = "comptes.Utilisateur"
LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "Africa/Dakar"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES":["rest_framework_simplejwt.authentication.JWTAuthentication"],
    "DEFAULT_PERMISSION_CLASSES":["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_SCHEMA_CLASS":"drf_spectacular.openapi.AutoSchema",
}
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME":timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME":timedelta(days=7),
}
CORS_ALLOWED_ORIGINS = [x.strip() for x in os.getenv(
    "CORS_ALLOWED_ORIGINS","http://localhost:4200").split(",") if x.strip()]
SPECTACULAR_SETTINGS = {"TITLE":"API Chantial","VERSION":"1.0.0"}
