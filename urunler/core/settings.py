import os
from pathlib import Path

# Projenin ana kök dizini (BASE_DIR)
BASE_DIR = Path(__file__).resolve().parent.parent

# Güvenlik Ayarları (Geliştirme aşaması için)
SECRET_KEY = 'django-insecure-your-secret-key-here'
DEBUG = True
ALLOWED_HOSTS = []

# Uygulama Tanımlamaları (Modern paneli sağlayan 'jazzmin' en üstte kalmalı)
INSTALLED_APPS = [
    'jazzmin',  # Modern yönetim paneli teması back to life!
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'kulucka.apps.KuluckaConfig', 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'

# 📌 VERİ TABANI AYARI (HATASIZ DOĞRU KULLANIM: 'NAME')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

#  GÜNCELLENECEK YENİ KOD:
AUTH_PASSWORD_VALIDATORS = []
# Dil ve Zaman Ayarları (Türkçe ve Türkiye Saati)
LANGUAGE_CODE = 'tr'
TIME_ZONE = 'Europe/Istanbul'
USE_I18N = True
USE_TZ = True

# Statik Dosya Ayarları (CSS, JS)
STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 📸 RESİMLERİN YÜKLENECEĞİ MEDYA AYARLARI
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 🎨 MODERN PANEL (JAZZMIN) ÖZELLEŞTİRMELERİ
JAZZMIN_SETTINGS = {
    "site_title": "Zanaat-AI Yönetim Paneli",
    "site_header": "Zanaat-AI Hub",
    "site_brand": "Zanaat-AI Yönetim",
    "welcome_sign": "Zanaat-AI Hub Yönetim Paneline Hoş Geldiniz",
    "search_model": ["auth.User", "kulucka.Urun"],
    "show_sidebar": True,
    "navigation_expanded": True,
    "order_with_respect_to": ["auth", "kulucka"],
    
    # 🔗 TAM İSTEDİĞİN ANA SAYFA BAĞLANTISI (ÜST SAĞ KÖŞEYE BUTON EKLER)
    "topmenu_links": [
        {"name": "Ana Sayfaya Git", "url": "kulucka:index", "new_window": True},
    ],
    
    "icons": {
        "auth.user": "fas fa-users",
        "kulucka.profil": "fas fa-user-shield",
        "kulucka.urun": "fas fa-shopping-bag",
    },
}

JAZZMIN_UI_CHANGES = {
    "theme": "flatly",  # Temiz ve modern bir e-ticaret görünümü
    "dark_mode_theme": "darkly",
}
# Django'ya giriş sayfamızın adresini öğretiyoruz
LOGIN_URL = '/giris/'