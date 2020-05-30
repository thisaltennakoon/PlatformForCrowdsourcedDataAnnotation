"""
Django settings for CrowdsourcedDataAnnotationPlatform project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'mgqr+xmp@v=y+6-ohs8t6cy9j841(j012agi=6$3r(-9(mf@cz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'UserManagement',
    'CreateDataAnnotationTask',
    'CreateDataGenerationTask',
    'DoDataAnnotationTask',
    'DoDataGenerationTask',
    'django_filters',
    'CreateTextDataAnnotationTask',
    'DoTextDataAnnotationTask',
    'DoTask',
    'CreateTask',
    'ImageDataAnalyse',
    'TextDataAnalyse',
    'testresultrank',
]
CRISPY_TEMPLATE_PACK = 'bootstrap4'
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'CrowdsourcedDataAnnotationPlatform.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'CrowdsourcedDataAnnotationPlatform.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

#Janani's database
"""DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cdap_usermanagement',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306'
    }
}"""


#Thisal's Postgres databsse
"""DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'CrowdsourcedDataAnnotationPlatform',
        'USER': 'postgres',
        'PASSWORD': '1234',
        'HOST':'localhost'
    }
}"""

#Thisal's Mysql databsse
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'crowdsourceddataannotationplatform',
        'USER': 'root',
        'PASSWORD': '',
        'HOST':'127.0.0.1',
        'PORT':'3308'
    }
}

#MySQL event for release data instances
"""
drop database crowdsourceddataannotationplatform;

create database crowdsourceddataannotationplatform;

use crowdsourceddataannotationplatform;

show tables;

select * from createtask_mediadatainstance;  

select * from createtask_textdatainstance; 

SET GLOBAL event_scheduler = ON; -- enable event scheduler.
SELECT @@event_scheduler;  -- check whether event scheduler is ON/OFF
CREATE EVENT release_data_instances_mediadatainstance  -- create your event
    ON SCHEDULE
      EVERY 300 SECOND  -- run every 300 secs (5 Min)
    DO
      UPDATE crowdsourceddataannotationplatform.createtask_mediadatainstance SET IsViewing=False,WhoIsViewing=0 WHERE IsViewing=True AND LastUpdate<= DATE_SUB(NOW(), INTERVAL 5 MINUTE)-- update this table
;
      
CREATE EVENT release_data_instances_textdatainstance  -- create your event
    ON SCHEDULE
      EVERY 300 SECOND  -- run every 300 secs (5 Min)
    DO
      UPDATE crowdsourceddataannotationplatform.createtask_textdatainstance SET IsViewing=False,WhoIsViewing=0 WHERE IsViewing=True AND LastUpdate<= DATE_SUB(NOW(), INTERVAL 5 MINUTE)-- update this table
;

delimiter //
CREATE TRIGGER set_last_update_time_mediadatainstance_on_update
    BEFORE UPDATE ON createtask_mediadatainstance
    FOR EACH ROW
    BEGIN
    SET NEW.LastUpdate = NOW();
    END; // 
    delimiter ;

    
delimiter //
CREATE TRIGGER set_last_update_time_mediadatainstance_on_insert
    BEFORE INSERT ON createtask_mediadatainstance
    FOR EACH ROW
    BEGIN
    SET NEW.LastUpdate = NOW();
    END; // 
    delimiter ;

delimiter //
CREATE TRIGGER set_last_update_time_textdatainstance_on_update
    BEFORE UPDATE ON createtask_textdatainstance
    FOR EACH ROW
    BEGIN
    SET NEW.LastUpdate = NOW();
    END; // 
    delimiter ;

    
delimiter //
CREATE TRIGGER set_last_update_time_textdatainstance_on_insert
    BEFORE INSERT ON createtask_textdatainstance
    FOR EACH ROW
    BEGIN
    SET NEW.LastUpdate = NOW();
    END; // 
    delimiter ;

"""

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS =  [
    os.path.join(BASE_DIR  , 'static')
]

STATIC_ROOT = os.path.join(BASE_DIR  , 'assets')

MEDIA_URL = '/images/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/images')

DJANGORESIZED_DEFAULT_SIZE = [1920, 1080]
DJANGORESIZED_DEFAULT_QUALITY = 75
DJANGORESIZED_DEFAULT_KEEP_META = True
DJANGORESIZED_DEFAULT_FORCE_FORMAT = 'JPEG'
DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {'JPEG': ".jpg"}
DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION = True

#   SMTP configuration

EMAIL_BACKEND = 'django.core.mail.backend.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = 'true'
EMAIL_HOST_USER = 'cdapmanager@gmail.com'
EMAIL_HOST_PASSWORD = 'cdap@admin'
