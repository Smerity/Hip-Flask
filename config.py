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

class Development(BaseConfig):
  DEBUG = True

  ## SQLAlchemy
  SQLALCHEMY_DATABASE_URI = "sqlite:///sqlite.db"

class Production(BaseConfig):
  DEBUG = False

  ## SQLAlchemy
  SQLALCHEMY_DATABASE_URI = "mysql://..."

class TestingConfig(Development):
  TESTING = True
