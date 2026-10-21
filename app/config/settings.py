
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(name, default=False):
    return os.getenv(name, str(default)).lower() in {"1", "true", "yes", "on"}


SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "unsafe-dev-key-change-me")
DEBUG = env_bool("DEBUG", False)

ALLOWED_HOSTS = [
    x.strip()
    for x in os.getenv(
        "ALLOWED_HOSTS", "localhost,127.0.0.1"
    ).split(",")
    if x.strip()
]

# CSRF: cho phép các địa chỉ HTTP hiện tại và HTTPS qua Nginx.
CSRF_TRUSTED_ORIGINS = [
    x.strip()
    for x in os.getenv(
        "CSRF_TRUSTED_ORIGINS", "http://localhost:8000"
    ).split(",")
    if x.strip()
]

for origin in [
    "https://localhost:8443",
    "https://127.0.0.1:8443",
]:
    if origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(origin)

# Nginx ghi đè X-Forwarded-Proto bằng giao thức thực tế.
# Chỉ tin cậy header này khi yêu cầu đi qua reverse proxy đáng tin cậy.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "appointments",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "config.wsgi.application"

# PostgreSQL: Django sử dụng tài khoản riêng, ít đặc quyền.
# Ưu tiên DJANGO_DB_USER và DJANGO_DB_PASSWORD.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "appointment_db"),
        "USER": os.getenv(
            "DJANGO_DB_USER",
            os.getenv("POSTGRES_USER", "app_user")
        ),
        "PASSWORD": os.getenv(
            "DJANGO_DB_PASSWORD",
            os.getenv("POSTGRES_PASSWORD", "")
        ),
        "HOST": os.getenv("POSTGRES_HOST", "db"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
        "CONN_MAX_AGE": 60,
        "OPTIONS": {"connect_timeout": 5},
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"
    },
]

LANGUAGE_CODE = "vi"
TIME_ZONE = "Asia/Ho_Chi_Minh"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = "/vol/web/static"
STATICFILES_DIRS = (
    [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []
)

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Security Headers
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "SAMEORIGIN"
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

# Cookie security
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage"
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
    },
}

# Logging: ghi log Django vào file để Promtail thu thập và gửi đến Loki.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "{asctime} {levelname} {name} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "appointment_file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "/var/log/appointment/django.log",
            "formatter": "standard",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["appointment_file"],
            "level": "INFO",
            "propagate": True,
        },
        "appointments": {
            "handlers": ["appointment_file"],
            "level": "INFO",
            "propagate": True,
        },
    },
}
