import flask

from app import app, oid

import models
import forms

@app.before_request
def lookup_current_user():
  flask.g.user = None
  # TODO: Sessions should be server backed so that compromised user cookies present no major issue
  if "user_id" in flask.session:
    flask.g.user = models.User.query.get(flask.session["user_id"])

@app.route("/login", methods=["GET", "POST"])
@oid.loginhandler
def login():
  if flask.g.user is not None:
    return flask.redirect(oid.get_next_url())
  if flask.request.method == "POST":
    openid = flask.request.form.get("openid")
    if openid:
      return oid.try_login(openid, ask_for=["email", "fullname", "nickname"])
  # Display the errors on the page using the standard flash mechanism
  error = oid.fetch_error()
  if error:
    flask.flash(error, "alert-error")
  return flask.render_template("login.html", next=oid.get_next_url())

@oid.after_login
def create_or_login(resp):
  u = models.User.query.filter_by(openid=resp.identity_url).first()

  # If u is None, a new user needs to be created
  # Otherwise, log in the existing user
  if not u:
    data = dict(username=resp.nickname, fullname=resp.fullname, email=resp.email, openid=resp.identity_url)
    flask.session["temp_login_details"] = data
    return flask.redirect(flask.url_for("create_profile", next=oid.get_next_url()))

  flask.session["user_id"] = u.id
  flask.flash(u"Successfully logged in", "alert-success")
  return flask.redirect(oid.get_next_url())

@app.route("/create", methods=['get', 'post'])
def create_profile():
  if flask.g.user is not None:
    return flask.redirect(flask.url_for('index'))

  data = None
  if "temp_login_details" in flask.session:
    data = flask.session["temp_login_details"]
    flask.session.pop("temp_login_details", None)
  result = forms.create_or_update_model(models.User, None, data)
  if "success" not in result:
    return flask.render_template("forms/add_create.html", **result)

  u = result["model"]
  flask.session["user_id"] = u.id
  flask.flash(u"Welcome to the site!", "alert-success")
  return flask.redirect(oid.get_next_url())

@app.route("/logout")
def logout():
    flask.session.pop("user_id", None)
    flask.flash(u"You were signed out", "alert-success")
    return flask.redirect(flask.url_for("index"))
