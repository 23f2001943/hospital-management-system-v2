import os
from dotenv import load_dotenv
load_dotenv()

class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT")
    SECURITY_PASSWORD_HASH="argon2"
    #SECURITY_JOIN_USER_ROLE = True

class LocalDevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.sqlite3"
    
    CELERY_BROKER_URL = os.environ.get("CACHE_REDIS_URL")
    CELERY_RESULT_BACKEND = os.environ.get("CACHE_REDIS_URL")

    MAIL_SERVER = "localhost"
    MAIL_PORT = 1025
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    MAIL_DEFAULT_SENDER = "test@hms.com"

    CACHE_TYPE = "RedisCache"
    CACHE_DEFAULT_TIMEOUT = 300   # 5 minutes
    CACHE_REDIS_URL = os.environ.get("CACHE_REDIS_URL")


class ProductionConfig(BaseConfig):
    DEBUG = False
