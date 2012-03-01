class BaseConfig(object):
  # Application Information
  SECRET_KEY = "3.14159"
  SESSION_COOKIE_NAME = "__session_x"

  # Email Settings
  ## By default we assume a Gmail account whilst getting off the ground
  MAIL_SERVER="smtp.gmail.com"
  MAIL_PORT=465
  MAIL_USE_SSL=True
  MAIL_USERNAME = "user@gmail.com"
  MAIL_PASSWORD = "..."

  # Flask-Sijax setup
  SIJAX_JSON_URI = "static/js/json2.js"
  SIJAX_STATIC_PATH = "static/js/sijax/"

class Development(BaseConfig):
  DEBUG = True

  ## SQLAlchemy
  SQLALCHEMY_DATABASE_URI = "sqlite:///sqlite.db"

  ### Cache
  CACHE_TYPE = "simple"
  # By default, cache for 3 minutes
  CACHE_DEFAULT_TIMEOUT = 3 * 60

class Production(BaseConfig):
  DEBUG = False

  ## SQLAlchemy
  SQLALCHEMY_DATABASE_URI = "mysql://..."

  ### Cache
  ## Upgrade to Memcache, Redis or similar in Production
  CACHE_TYPE = "simple"
  # By default, cache for 3 minutes
  CACHE_DEFAULT_TIMEOUT = 3 * 60

class TestingConfig(Development):
  TESTING = True
