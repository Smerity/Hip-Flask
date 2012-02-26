import flask

from app import app, oid

@app.before_request
def lookup_current_user():
  flask.g.user = None
  if "user" in flask.session:
    flask.g.user = flask.session["user"]

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
  # TODO: You'd likely want more details and to store the user permanently
  flask.session["user"] = {"fullname": resp.fullname, "email": resp.email, "nickname": resp.nickname}
  flask.flash(u"Successfully signed in", "alert-success")
  return flask.redirect(oid.get_next_url())

@app.route("/logout")
def logout():
    flask.session.pop("user", None)
    flask.flash(u"You were signed out", "alert-success")
    return flask.redirect(flask.url_for("index"))
