import os
gettext = lambda s: s
DATA_DIR = os.path.dirname(os.path.dirname(__file__))
"""
Django settings for ROOT project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'w#!_7ufj2_m8745@a%4z8m^+&2lx46-2r*stqmme0v%#mb)fm@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition





ROOT_URLCONF = 'ROOT.urls'

WSGI_APPLICATION = 'ROOT.wsgi.application'

UPLOAD_PATH = 'static/uploads/noticia/'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases



# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'eng'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(DATA_DIR, 'media')
STATIC_ROOT = os.path.join(DATA_DIR, 'static')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'ROOT', 'static_local'),
)
SITE_ID = 1

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler",
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.i18n',
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.csrf',
    'django.core.context_processors.tz',
    'sekizai.context_processors.sekizai',
    'django.core.context_processors.static',
    'cms.context_processors.cms_settings'
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'ROOT', 'templates'),
)

INSTALLED_APPS = (
    'djangocms_admin_style',
    'djangocms_text_ckeditor',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'cms',
    'menus',
    'sekizai',
    'mptt',
    'djangocms_style',
    'djangocms_column',
    'djangocms_file',
    'djangocms_flash',
    'djangocms_googlemap',
    'djangocms_inherit',
    'djangocms_link',
    'djangocms_picture',
    'djangocms_teaser',
    'djangocms_video',
    'south',
    'reversion',
    'ROOT',
    'ROOT.rmais'
)

LANGUAGES = (
    ## Customize this
    ('eng', gettext('eng')),
)

CMS_LANGUAGES = {
    ## Customize this
    'default': {
        'public': True,
        'hide_untranslated': False,
        'redirect_on_fallback': True,
    },
    1: [
        {
            'public': True,
            'code': 'eng',
            'hide_untranslated': False,
            'name': gettext('eng'),
            'redirect_on_fallback': True,
        },
    ],
}

CMS_TEMPLATES = (
    ## Customize this
    ('page.html', 'Page'),
    ('feature.html', 'Page with Feature')
)

CMS_PERMISSION = True

CMS_PLACEHOLDER_CONF = {}

DATABASES = {
    # 'default':
    #     {
    #     'ENGINE': 'django.db.backends.sqlite3', 
    #     'NAME': 'project.db', 
    #     'HOST': 'localhost', 
    #     'USER': '', 
    #     'PASSWORD': '', 
    #     'PORT': ''
    # }
    # ,
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'radarmais_d',
        'USER': 'root',
        'PASSWORD': 'y8TF4Va1P2',
        'HOST': 'mysql-zoio-bancos.jelastic.websolute.net.br',
        'PORT': '3306',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # em caso smtp

from .email_info import EMAIL_USE_TLS, EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_PORT

EMAIL_USE_TLS = EMAIL_USE_TLS
EMAIL_HOST = EMAIL_HOST
EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
EMAIL_PORT = EMAIL_PORT

ADMINS = {
    ('webmaster', 'rodrigo.costa@zoio.net.br')
}
