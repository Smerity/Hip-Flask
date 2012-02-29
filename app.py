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

app = flask.Flask(__name__)
# Enables the "with" keyword extension in Jinja2
app.jinja_env.add_extension("jinja2.ext.with_")

# Flask Config Setup
####################
if app.debug:
  app.config.from_object("config.Development")
  logging.warn("Running in development mode...")
else:
  app.config.from_object("config.Production")
  file_handler = SysLogHandler()
  file_handler.setLevel(logging.WARNING)
  app.logger.addHandler(file_handler)

# Flask Extensions Setup
########################
import flask_extensions
cache = Cache(app)
db = SQLAlchemy(app)
flask_sijax.Sijax(app)
# In production, the OpenID backend should be changed from the default FileStore
oid = OpenID(app, "./openid_store")
SafeSessions(app)
if app.config["MAIL_SERVER"]:
  mail=Mail(app)

# Views
#######
import admin
app.register_blueprint(admin.admin_console, url_prefix="/admin")
import oid
import views
