# General imports
import flask
import logging
from logging.handlers import SysLogHandler

# Flask imports
import flask_sijax
from flaskext.cache import Cache
from flaskext.lesscss import lesscss
from flaskext.mail import Mail
from flaskext.openid import OpenID
from flaskext.sqlalchemy import SQLAlchemy
##
from safe_session import SafeSessions

# Flask Config Setup
####################
def create_app(debug=False, config=None):
  app = flask.Flask(__name__)
  if config:
    # Useful for tests
    app.config.from_object(config)
  elif debug:
    # Development mode
    app.config.from_object("config.Development")
    logging.warn("Running in development mode...")
  else:
    # Production mode
    app.config.from_object("config.Production")
    file_handler = SysLogHandler()
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)

  # Enables the "with" keyword extension in Jinja2
  app.jinja_env.add_extension("jinja2.ext.with_")

  return app

app = create_app(debug=True)

# Flask Extensions Setup
########################
cache = Cache(app)
db = SQLAlchemy(app)
flask_sijax.Sijax(app)
# In production, the OpenID backend should be changed from the default FileStore
oid = OpenID(app, "./openid_store")
SafeSessions(app)
if "MAIL_SERVER" in app.config:
  mail=Mail(app)
##
import flask_extensions

# Views
#######
import admin
app.register_blueprint(admin.admin_console, url_prefix="/admin")
import oid
import forms
import models
import views
