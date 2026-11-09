import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-me")
DEBUG = os.environ.get("DEBUG", "False") == "True"
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")

INSTALLED_APPS = ["notes"]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": []},
}]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",  # this engine also works for MariaDB
        "NAME": os.environ.get("DB_NAME", "notesdb"),
        "USER": os.environ.get("DB_USER", "notes_user"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "notes_pass"),
        "HOST": os.environ.get("DB_HOST", "127.0.0.1"),
        "PORT": os.environ.get("DB_PORT", "3306"),
        "OPTIONS": {"charset": "utf8mb4"},
    }
}

APPEND_SLASH = False  # keeps URLs exactly like the Node app: /notes, not /notes/
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
USE_TZ = True