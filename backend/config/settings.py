"""
Django settings for ESC Shipping backend.

Uses python-decouple for environment variable management.
Copy .env.example to .env and adjust values as needed.
"""

from pathlib import Path
from datetime import timedelta
from decouple import config, Csv

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent


def configured_path(name, default):
    """Resolve an environment path relative to the Django backend directory."""
    value = Path(config(name, default=str(default)))
    return value if value.is_absolute() else BASE_DIR / value


def configured_url(name, default):
    """Normalize an asset URL so Django always receives an absolute path."""
    value = config(name, default=default).strip()
    return f"/{value.strip('/')}/"

# =============================================================================
# Core Settings
# =============================================================================

SECRET_KEY = config("DJANGO_SECRET_KEY", default="django-insecure-dev-key")
DEBUG = config("DJANGO_DEBUG", default=True, cast=bool)
ALLOWED_HOSTS = config(
    "DJANGO_ALLOWED_HOSTS",
    default="localhost,127.0.0.1,website.ex-shipping.com,www.website.ex-shipping.com",
    cast=Csv(),
)

# When Django is behind a reverse proxy (Nginx, Apache or a hosting panel),
# preserve the original HTTPS scheme and host forwarded by that proxy.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = config("DJANGO_USE_X_FORWARDED_HOST", default=False, cast=bool)
SECURE_SSL_REDIRECT = config("DJANGO_SECURE_SSL_REDIRECT", default=False, cast=bool)
SESSION_COOKIE_SECURE = config("DJANGO_SESSION_COOKIE_SECURE", default=not DEBUG, cast=bool)
CSRF_COOKIE_SECURE = config("DJANGO_CSRF_COOKIE_SECURE", default=not DEBUG, cast=bool)

# =============================================================================
# Application Definition
# =============================================================================

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "django_filters",
    "drf_spectacular",
]

LOCAL_APPS = [
    "apps.users",
    "apps.cms",
    "apps.devis",
    "apps.shipping",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# =============================================================================
# Middleware
# =============================================================================

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# =============================================================================
# URL Configuration
# =============================================================================

ROOT_URLCONF = "config.urls"

# =============================================================================
# Templates
# =============================================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# =============================================================================
# WSGI / ASGI
# =============================================================================

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# =============================================================================
# Database (SQLite for dev, PostgreSQL for production)
# =============================================================================

DB_ENGINE = config("DB_ENGINE", default="sqlite")

if DB_ENGINE == "postgresql":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": config("DB_NAME", default="esc_shipping"),
            "USER": config("DB_USER", default="postgres"),
            "PASSWORD": config("DB_PASSWORD", default="postgres"),
            "HOST": config("DB_HOST", default="localhost"),
            "PORT": config("DB_PORT", default="5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# =============================================================================
# Password Validation
# =============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# =============================================================================
# Internationalization
# =============================================================================

LANGUAGE_CODE = "fr"
LANGUAGES = [
    ("fr", "Français"),
    ("en", "English"),
]
LOCALE_PATHS = [
    BASE_DIR / "locale",
]
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# =============================================================================
# Static & Media Files
# =============================================================================

# Static files are collected once and served by WhiteNoise (or the web server).
# Keep STATIC_ROOT separate from application source directories.
STATIC_URL = configured_url("DJANGO_STATIC_URL", "/static/")
STATIC_ROOT = configured_path("DJANGO_STATIC_ROOT", BASE_DIR / "staticfiles")

# Uploaded files (CMS images, partner logos, service images, etc.) are media,
# not static assets. In production this directory should be on persistent
# storage and served by the reverse proxy or object storage.
MEDIA_URL = configured_url("DJANGO_MEDIA_URL", "/media/")
MEDIA_ROOT = configured_path("DJANGO_MEDIA_ROOT", BASE_DIR / "media")

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# =============================================================================
# Default Primary Key Field Type
# =============================================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# =============================================================================
# Custom User Model
# =============================================================================

AUTH_USER_MODEL = "users.User"

# =============================================================================
# Django REST Framework
# =============================================================================

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# =============================================================================
# SimpleJWT Configuration
# =============================================================================

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=config("ACCESS_TOKEN_LIFETIME_MINUTES", default=60, cast=int)
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=config("REFRESH_TOKEN_LIFETIME_DAYS", default=7, cast=int)
    ),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
}

# =============================================================================
# CORS Configuration
# =============================================================================

CORS_ALLOW_ALL_ORIGINS = config("CORS_ALLOW_ALL_ORIGINS", default=DEBUG, cast=bool)
CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS", default="", cast=Csv())
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", default="", cast=Csv())

# Enable this only when the hosting platform does not provide a separate
# static/media mapping. Nginx/Apache or object storage is preferred in prod.
SERVE_MEDIA = config("DJANGO_SERVE_MEDIA", default=DEBUG, cast=bool)

# =============================================================================
# Email Configuration (SMTP)
# =============================================================================

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST", default="mail.ex-shipping.com")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="website@ex-shipping.com")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_USE_SSL = config("EMAIL_USE_SSL", default=False, cast=bool)
EMAIL_TIMEOUT = config("EMAIL_TIMEOUT", default=30, cast=int)

DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="website@ex-shipping.com")
ADMIN_EMAIL = config("ADMIN_EMAIL", default="website@ex-shipping.com")

# =============================================================================
# drf-spectacular (API Documentation)
# =============================================================================

SPECTACULAR_SETTINGS = {
    "TITLE": "ESC Shipping API",
    "DESCRIPTION": "Backend API for ESC Shipping management system",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}
