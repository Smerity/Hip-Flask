class Development(object):
  DEBUG = True
  TESTING = False
  SQLALCHEMY_DATABASE_URI = "sqlite:///sqlite.db"

class Production(Development):
  DEBUG = False
  SQLALCHEMY_DATABASE_URI = "mysql://..."

class TestingConfig(Development):
  TESTING = True
