from app import app, db

from datetime import datetime
import flask
import sqlalchemy

import flaskext.wtf as wtf

from forms import create_or_update_model

class AlchemyExtensions(object):
  @classmethod
  def props(kls):
    """Return the properties of the SQLAlchemy model"""
    from sqlalchemy.orm.properties import RelationshipProperty
    return [x.key for x in kls.__mapper__.iterate_properties if type(x) != RelationshipProperty]

class User(db.Model, AlchemyExtensions):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, index=True, nullable=False)
  fullname = db.Column(db.String(120))
  email = db.Column(db.String(120), unique=True, nullable=False)
  registered = db.Column(db.DateTime)
  openid = db.Column(db.String(250), unique=True, index=True, nullable=False)
  admin = db.Column(db.Boolean, default=False, nullable=False)

  def __init__(self):
    registered = datetime.utcnow()

  @property
  def name():
    return "%s" % self.fullname if self.fullname else self.username

  def __repr__(self):
    return "<User: %r>" % self.username

  class Form(wtf.Form):
    ordered_fields = ["username", "fullname", "email", "admin"]
    username = wtf.TextField("Username", [wtf.validators.Length(min=4, max=26)])
    fullname = wtf.TextField("Full Name", [wtf.validators.Length(min=5, max=70)])
    email = wtf.TextField("Email", [wtf.validators.Email()])
    admin = wtf.BooleanField("Set as Admin")

    openid = wtf.HiddenField("OpenID")

    def validate_username(self, field):
      if not field.data:
        raise wtf.ValidationError, "You must supply a username"
      if User.query.filter_by(username=field.data).count():
        raise wtf.ValidationError, "The given username is already in use"

    def validate_email(self, field):
      if User.query.filter_by(email=field.data).count():
        raise wtf.ValidationError, "That email address has previously been used"

    def validate_admin(self, field):
      if field.data:
        raise wtf.ValidationError, "Uhm... Seriously, dude, we were joking... <strong>No admin for you!</strong>"

@app.route("/add_user", methods=["GET", "POST"])
def add_user():
  if not flask.g.user:
    flask.flash("You can only update your details if you're logged in!", "alert-error")
    return flask.redirect(flask.url_for("index"))
  result = create_or_update_model(flask.g.user)
  if result is True:
    flask.flash("Your details have been uccessfully updated", "alert-success")
    return flask.redirect(flask.url_for("index"))
  return flask.render_template("forms/add_create.html", **result)
