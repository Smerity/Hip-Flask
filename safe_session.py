# Majority of code pulled from http://flask.pocoo.org/snippets/51/

from werkzeug.datastructures import CallbackDict
from flask.sessions import SessionInterface, SessionMixin
from itsdangerous import URLSafeSerializer, URLSafeTimedSerializer, BadSignature

import pickle

class ItsdangerousSession(CallbackDict, SessionMixin):
  def __init__(self, initial=None):
    def on_update(self):
      self.modified = True
    CallbackDict.__init__(self, initial, on_update)
    self.modified = False

class SafeSessions(SessionInterface):
  session_class = ItsdangerousSession

  def __init__(self, app, salt="flasksaltysession"):
    self.salt = salt
    app.session_interface = self

  def get_serializer(self, app):
    if not app.secret_key:
      return None
    # Pickle serializiation is used as a number of projects require Python object compatibility
    # This can trivially be replaced with a JSON serializer if appropriate
    return URLSafeTimedSerializer(app.secret_key, salt=self.salt, serializer=pickle)

  def open_session(self, app, request):
    s = self.get_serializer(app)
    if s is None:
      return None
    val = request.cookies.get(app.session_cookie_name)
    if not val:
      return self.session_class()

    # A Get Total Seconds function is required for Python < 2.7
    def get_total_seconds(td): return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 1e6) / 1e6
    max_age = get_total_seconds(app.permanent_session_lifetime)

    try:
      data = s.loads(val, max_age=max_age)
      return self.session_class(data)
    except BadSignature:
      return self.session_class()

  def save_session(self, app, session, response):
    domain = self.get_cookie_domain(app)
    if not session:
      if session.modified:
        response.delete_cookie(app.session_cookie_name, domain=domain)
      return
    expires = self.get_expiration_time(app, session)
    val = self.get_serializer(app).dumps(dict(session))
    response.set_cookie(app.session_cookie_name, val, expires=expires, httponly=True, domain=domain)

ItsdangerousSessionInterface = SafeSessions
